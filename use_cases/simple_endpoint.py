import json
import re

from common_imports import *
from gooddata_pandas import GoodPandas
from gooddata_sdk import GoodDataSdk

app = slack_bolt.App(token=os.environ["SLACK_BOT_TOKEN"])
CONVERSATION_ID = None  # You can create and specify conversation_id to be used.
chatbot = Chatbot({"session_token": os.environ["CHATGPT_TOKEN"]}, conversation_id=CONVERSATION_ID)

sdk = GoodDataSdk.create(os.environ["GOODDATA_HOST"], os.environ["GOODDATA_TOKEN"])
pandas = GoodPandas(os.environ["GOODDATA_HOST"], os.environ["GOODDATA_TOKEN"])
df_factory = pandas.data_frames(os.environ["GOODDATA_WORKSPACE_ID"])


def feed_chatbot():
    """
    Teach the chatbot a simple endpoint definition.

    e.g. I have the following API request body {'attributes': ['string'], 'facts': ['string'], 'metrics': ['string']}
    """
    request_body = "{'attributes': ['string'], 'facts': ['string'], 'metrics': ['string']}"
    chatbot.ask(f"I have the following API request body {request_body}", conversation_id=CONVERSATION_ID)


def fill_the_endpoint(msg: str) -> tuple[bool, dict]:
    """
    The chatbot can fill the API request body from the given sentence.

    e.g. Can you fill the API request body from the following sentence:
        Show me visualization of campaign name attribute, quantity fact, and revenue metric.
    """
    template = f"Can you fill the API request body from the following sentence: {msg}"
    response = chatbot.ask(template, conversation_id=CONVERSATION_ID)
    regex = r"\`\`\`(.*)\`\`\`"
    matches = re.search(regex, response["message"].replace("\n", "\\n"))
    if matches:
        request_body = matches.group(1).replace("\\n", "").replace("\\", "")
        return True, json.loads(request_body)
    return False, {}


def get_data(mapping: dict) -> str:
    """
    Help function to get data from the mapping.

    e.g. get_data({"attributes": ["Region"], "facts": ["Quantity"], "metrics": ["Revenue"]})
    """
    model = sdk.catalog_workspace.get_declarative_workspace(os.environ["WORKSPACE_ID"])
    attributes = {}
    facts = {}
    for d in model.ldm.datasets:
        for a in d.attributes:
            attributes[a.title] = a.id
        for f in d.facts:
            facts[f.title] = f.id
    metrics = {m.title: m.id for m in model.analytics.metrics}

    result = {}
    for k, v in mapping.items():
        for x in v:
            match k:
                case "attributes":
                    result[attributes[x]] = f"label/{attributes[x]}"
                case "facts":
                    result[facts[x]] = f"fact/{facts[x]}"
                case "metrics":
                    result[metrics[x]] = f"metric/{metrics[x]}"
    return df_factory.for_items(items=result).to_markdown(tablefmt="grid")


@app.event("app_mention")
def bot_is_mentioned(
    event: dict[str, Any],
    say: slack_bolt.context.context.Say,
):
    """
    In this use case, we can ask the chatbot to give us the report.
    Thanks to the fact that we feed the chatbot with a simple API request body.
    We can ask the chatbot if it could fill the API request body from the given sentence.
    The chatbot will be able to answer us.

    e.g. Please show me a table of Region attribute, Quantity fact, and Revenue metric.
    """
    message = event["text"].split(" ", 1)[1]
    flag, mapping = fill_the_endpoint(message)
    if flag:
        response = get_data(mapping)
        say(response)
    else:
        try:
            response = chatbot.ask(message, conversation_id=CONVERSATION_ID)
            say(response["message"])
        except Exception:  # noqa
            say("Sorry, I could not process your prompt. Please try it again.")


if __name__ == "__main__":
    feed_chatbot()
    SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()
