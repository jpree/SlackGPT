from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from .config import SLACK_BOT_TOKEN, SLACK_APP_TOKEN, logger
from .utils import process_message

class SlackBot:
    def __init__(self, chatbot):
        self.app = App(token=SLACK_BOT_TOKEN)
        self.chatbot = chatbot
        self.bot_user_id = self.app.client.auth_test()["user_id"]
        logger.info("Bot user ID: %s", self.bot_user_id)
        self.register_handlers()

    def register_handlers(self):
        @self.app.message(".*")
        def handle_mention(message, say):
            logger.info("Handling message mention")
            ts=message["ts"]
            message_text=message["text"]
            channel_id=message["channel"]
            chat_response = process_message(self.chatbot, self.app, message_text, channel_id, self.bot_user_id)
            say(chat_response)

        @self.app.event("app_mention")
        def handle_app_mention_events(body, say):
            logger.info("Handling app mention event")
            message_text = body["event"]["text"]
            channel_id = body["event"]["channel"]
            ts = body["event"]["ts"]
            chat_response = process_message(self.chatbot, self.app, message_text, channel_id, self.bot_user_id)
            say(chat_response)

    def start(self):
        try:
            logger.info("Starting the SocketModeHandler")
            SocketModeHandler(self.app, SLACK_APP_TOKEN).start()
        except Exception as e:
            logger.error(f"Error starting the SocketModeHandler: {e}")
