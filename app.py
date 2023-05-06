import os
import logging
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.chat_models import ChatOpenAI
from langchain.schema import AIMessage, HumanMessage

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Initialize the Slack app
def initialize_app():
    return App(token=os.environ.get("SLACK_BOT_TOKEN"))

app = initialize_app()

def initialize_chat_model():
    return ChatOpenAI(
        temperature=0.9,
        model_name="gpt-3.5-turbo",
        verbose=True
    )

chat_model = initialize_chat_model()

def get_chat_history(channel_id, bot_user_id):
    response = app.client.conversations_history(channel=channel_id, limit=10)

    messages = []
    for msg in response["messages"]:
        if msg['user'] == bot_user_id:
            messages.insert(0, AIMessage(content=msg['text']))
        else:
            messages.insert(0, HumanMessage(content=msg['text']))

    return messages

def get_bot_user_id():
    try:
        bot_user_id = app.client.auth_test()["user_id"]
        return bot_user_id
    except Exception as e:
        logger.error(f"Error retrieving bot user info: {e}")
        return None

def process_message(message_text, channel_id, bot_user_id):
    try:
        logger.debug(f"process_message: {message_text} {channel_id} {bot_user_id}")
        chat_history = get_chat_history(channel_id, bot_user_id)
        response = chat_model(chat_history)
        return response.content
    except Exception as e:
        logger.error(f"Error processing message: {e}")
        return "Sorry, something went wrong. Please try again later."

@app.message(".*")
def handle_mention(message, say, logger):
    logger.info("handle_mention")
    chat_response = process_message(message["text"], message["channel"], get_bot_user_id())
    say(chat_response)

@app.event("app_mention")
def handle_app_mention_events(body, say, logger):
    logger.debug("handle_app_mention_events")
    message_text = body["event"]["text"]
    channel_id = body["event"]["channel"]
    chat_response = process_message(message_text, channel_id, get_bot_user_id())
    say(chat_response)

if __name__ == "__main__":
    SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()
