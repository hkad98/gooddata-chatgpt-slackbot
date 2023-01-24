# How to run this demo

Requirements:
* Python 3.10+
* [GoodData Cloud](https://www.gooddata.com/trial/?utm_medium=blogpost&utm_source=medium.com&utm_campaign=gooddata_slack_chatgpt&utm_content=autor_jan) or [GoodData.CN CE](https://hub.docker.com/r/gooddata/gooddata-cn-ce/?utm_medium=blogpost&utm_source=medium.com&utm_campaign=gooddata_slack_chatgpt&utm_content=autor_jan)
* [Slack](https://slack.com/) with created [bot](https://slack.com/help/articles/115005265703-Create-a-bot-for-your-workspace#:~:text=A%20bot%20is%20a%20nifty,a%20bot%20for%20your%20workspace.)
* [ChatGPT](https://openai.com/blog/chatgpt/) account

To run this demo, you can use predefined commands in the Makefile command.
```bash
# Creates virtual environment and installs necessary dependencies
make dev
```

```bash
# Create .env file
touch .env

# Fill .env with the following keys with relevant values
# GOODDATA_HOST=
# GOODDATA_TOKEN=
# GOODDATA_WORKSPACE_ID=
# SLACK_APP_TOKEN=
# SLACK_BOT_TOKEN=
# CHATGPT_TOKEN=
```

How to get key for XYZ?
* GOODDATA_HOST – the whole string before the first "/" in the URL of your GoodData instance
* [GOODDATA_TOKEN](https://www.gooddata.com/developers/cloud-native/doc/cloud/getting-started/create-api-token/?utm_medium=blogpost&utm_source=medium.com&utm_campaign=gooddata_slack_chatgpt&utm_content=autor_jan)
* [GOODDATA_WORKSPACE_ID](https://www.gooddata.com/developers/cloud-native/doc/cloud/manage-deployment/manage-workspaces/api/objects-identification/#accessing-an-object-via-the-api/?utm_medium=blogpost&utm_source=medium.com&utm_campaign=gooddata_slack_chatgpt&utm_content=autor_jan)
* [SLACK_APP_TOKEN](https://api.slack.com/authentication/token-types#app)
* [SLACK_BOT_TOKEN](https://api.slack.com/authentication/token-types#bot)
* [CHATGPT_TOKEN](https://github.com/acheong08/ChatGPT/wiki/Setup#authentication)

After everything is set up, you can try to call scripts in [use_cases](use_cases) directory.
e.g. `python use_cases/pure_integration.py`.
Do not forget to activate your virtual environment before running the script from the command line! ;)

You can activate virtual environment with the following script `source .venv/bin/activate`
