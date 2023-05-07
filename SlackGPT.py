import os
import logging
from chatbot import ChatBot
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

# config
persona_token = "&lt;persona&gt;"

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

chatbot = ChatBot("gpt-3.5-turbo", 0.9)
app = App(token=os.environ.get("SLACK_BOT_TOKEN"))

#chat_model = initialize_chat_model()
def get_purpose(channel_id):
    channel_purpose = "You are a friendly and helpful Chatbot."
    try:
        # Call the conversations.info method using the WebClient
        response = app.client.conversations_info(channel=channel_id)
        # Check if the API call was successful
        if response['ok']:
            logger.info("Detected channel persona")
            if response['channel']['purpose']['value'].startswith(persona_token):
                channel_purpose = response['channel']['purpose']['value'][len(persona_token):]
                channel_purpose=chatbot.get_prompt(channel_purpose)
                logger.info("added personal to template")
    except Exception as e:
        logger.error("Error in get_purpose", exc_info=1)
    return(channel_purpose)
    
def get_chat_history(channel_id, bot_user_id):
    response = app.client.conversations_history(channel=channel_id, limit=10)
    prompt=get_purpose(channel_id)
    messages = []
    for msg in response["messages"]:
        if msg['user'] == bot_user_id:
            messages.insert(0, chatbot.get_ai_message(msg['text']))
        else:
            messages.insert(0, chatbot.get_user_message(msg['text']))
    messages.insert(0, chatbot.get_system_message(prompt))
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
        response = chatbot.chat(chat_history)
        return response.content
    except Exception as e:
        logger.error(f"Error processing message: {e}")
        return "Sorry, something went wrong. Please try again later."
    
@app.message(".*")
def handle_mention(message, say):
    logger.info("handle_mention")
    chat_response = process_message(message["text"], message["channel"], get_bot_user_id())
    say(chat_response)

@app.event("app_mention")
def handle_app_mention_events(body, say):
    logger.debug("handle_app_mention_events")
    message_text = body["event"]["text"]
    channel_id = body["event"]["channel"]
    chat_response = process_message(message_text, channel_id, get_bot_user_id())
    say(chat_response)

if __name__ == "__main__":
    SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()