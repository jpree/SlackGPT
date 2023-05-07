import os
import logging
from chatbot import ChatBot
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

# config
persona_token = "&lt;persona&gt;"
included_chat_history = 1
bot_user_id = "U0561DSLA3U"

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

chatbot = ChatBot("gpt-3.5-turbo", 0.9)
app = App(token=os.environ.get("SLACK_BOT_TOKEN"))

def get_purpose(channel_id):
    channel_purpose = f"You are a friendly and helpful slackbot. Your slack user id is: '{bot_user_id}'. When you encounter an ID, such as 'U12345678', it's a Slack user and you can use it to mention that user by including <@U12345678> in your message. Mention the user when you want to be sure you get their attention or to emphasize something to them. You can also do anything allowed in slack text like: formatting text as bold, italic, or strikethrough, including code blocks with triple backticks, adding links using < > symbols, and using emoji by typing the name of the emoji surrounded by colons."
    try:
        # Call the conversations.info method using the WebClient
        response = app.client.conversations_info(channel=channel_id)
        # Check if the API call was successful
        if response['ok']:
            logger.info("Detected channel persona")
            # Check if the 'purpose' key exists in the response dictionary
            if 'purpose' in response['channel']:
                if response['channel']['purpose']['value'].startswith(persona_token):
                    channel_purpose = response['channel']['purpose']['value'][len(persona_token):]
                    channel_purpose=chatbot.get_prompt(channel_purpose)
                    logger.info("added personal to template")
    except Exception as e:
        logger.error("Error in get_purpose", exc_info=1)
    return(channel_purpose)
    
def get_chat_history(channel_id, bot_user_id):
    response = app.client.conversations_history(channel=channel_id, limit=included_chat_history)
    prompt=get_purpose(channel_id)
    messages = []
    for msg in response["messages"]:
        message=f"{msg['user']}:{msg['text']}"
        if msg['user'] == bot_user_id:
            messages.insert(0, chatbot.get_ai_message(msg['text']))
        else:
            messages.insert(0, chatbot.get_user_message(message))
        logger.debug(message)
    messages.insert(0, chatbot.get_system_message(prompt))
    return messages

# def get_bot_user_id():
#     try:
#         bot_user_id = app.client.auth_test()["user_id"]
#         return bot_user_id
#     except Exception as e:
#         logger.error(f"Error retrieving bot user info: {e}")
#         return None
    
def process_message(message_text, channel_id):
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
    chat_response = process_message(message["text"], message["channel"])
    say(chat_response)

@app.event("app_mention")
def handle_app_mention_events(body, say):
    logger.debug("handle_app_mention_events")
    message_text = body["event"]["text"]
    channel_id = body["event"]["channel"]
    chat_response = process_message(message_text, channel_id)
    say(chat_response)

if __name__ == "__main__":
    SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()