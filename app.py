import os
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

# Initializes your app with your bot token and signing secret
app = App(
    token=os.environ.get("SLACK_BOT_TOKEN")
)
print(os.environ.get("SLACK_BOT_TOKEN"))
# Define a function to handle incoming messages that mention the bot
@app.message(".*")
def handle_mention(message, say, logger):
    print(message)
    
    # Get the text of the incoming message
    message_text = message["text"]

    # Respond to the message with "Hello, world!"
    say(f"Hello!")

# Start your app
if __name__ == "__main__":
    SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()
