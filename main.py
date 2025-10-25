import os
from datetime import datetime, date, timedelta
from dotenv import load_dotenv
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler


load_dotenv()


app = App(token=os.environ.get("SLACK_BOT_TOKEN"))
SLACK_CHANNEL_ID = os.environ.get("SLACK_CHANNEL_ID")

@app.command("/add-github")
def handle_add_github(ack, command, client):
    ack()

    github_handle = command['text'].strip()
    slack_user_id = command['user_id']

    if github_handle == "" or " " in github_handle:
        client.chat_postEphemeral(
            channel=SLACK_CHANNEL_ID,
            user=slack_user_id,
            text="Oops, your handle looks incorrect pls do it again `/add-github YourHandle`"
        )
        return

    client.chat_postEphemeral(
        channel=SLACK_CHANNEL_ID,
        user=slack_user_id,
        text="Cool you are in now, make sure to code & commit everyday :D"
    )

    print(f"github handle: '{github_handle}' from user: '{slack_user_id}'")

if __name__ == "__main__":

    print("Starting Slack Bot...")
    handler = SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"])
    handler.start()