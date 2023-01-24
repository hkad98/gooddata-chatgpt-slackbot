from common_imports import *

app = slack_bolt.App(token=os.environ["SLACK_BOT_TOKEN"])
CONVERSATION_ID = None  # You can create and specify conversation_id to be used.
chatbot = Chatbot({"session_token": os.environ["CHATGPT_TOKEN"]}, conversation_id=CONVERSATION_ID)


@app.event("app_mention")
def bot_is_mentioned(
    event: dict[str, Any],
    say: slack_bolt.context.context.Say,
):
    message = event["text"].split(" ", 1)[1]
    try:
        response = chatbot.ask(message, conversation_id=CONVERSATION_ID)
        say(response["message"])
    except Exception:  # noqa
        say("Sorry, I could not process your prompt. Please try it again.")


if __name__ == "__main__":
    SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()
