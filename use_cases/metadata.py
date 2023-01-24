from common_imports import *
from gooddata_sdk import GoodDataSdk

app = slack_bolt.App(token=os.environ["SLACK_BOT_TOKEN"])
CONVERSATION_ID = None  # You can create and specify conversation_id to be used.
chatbot = Chatbot({"session_token": os.environ["CHATGPT_TOKEN"]}, conversation_id=CONVERSATION_ID)
sdk = GoodDataSdk.create(os.environ["GOODDATA_HOST"], os.environ["GOODDATA_TOKEN"])


def feed_chatbot():
    workspaces = sdk.catalog_workspace.list_workspaces()
    chatbot.ask(str(workspaces))


@app.event("app_mention")
def bot_is_mentioned(
    event: dict[str, Any],
    say: slack_bolt.context.context.Say,
):
    """
    In this use case, we can ask the chatbot to give us the names of workspaces.
    Thanks to the fact that we feed the chatbot with metadata before.
    The chatbot will be able to answer us.

    e.g. Give me the names of workspaces
    """
    message = event["text"].split(" ", 1)[1]
    try:
        response = chatbot.ask(message, conversation_id=CONVERSATION_ID)
        say(response["message"])
    except Exception:  # noqa
        say("Sorry, I could not process your prompt. Please try it again.")


if __name__ == "__main__":
    feed_chatbot()
    SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()
