import os
import re
import logging
from chatbot import ChatBot
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

# config
persona_token = "&lt;persona&gt;"
included_chat_history = 1
bot_user_id = "U0561DSLA3U"
#reaction_prefix = ""

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

chatbot = ChatBot("gpt-3.5-turbo", 0.9)
app = App(token=os.environ.get("SLACK_BOT_TOKEN"))

def get_purpose(channel_id):
    channel_purpose = chatbot.get_default_prompt()
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
    return(channel_purpose.replace("{bot_user_id}", bot_user_id))
    
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

def react_message(channel, timestamp, emote):
    app.client.reactions_add(
        channel=channel,
        timestamp=timestamp,
        name=emote)

# def get_bot_user_id():
#     try:
#         bot_user_id = app.client.auth_test()["user_id"]
#         return bot_user_id
#     except Exception as e:
#         logger.error(f"Error retrieving bot user info: {e}")
#         return None
def extract_and_add_reaction(text, channel, ts):
    # Search for the reaction token using a regular expression
    match = re.search(r'~\w+~$', text)
    if match:
        reaction_token = match.group(0)
        # Remove the delimiter characters from the reaction token
        reaction_name = reaction_token[1:-1]
        # Remove the reaction token from the message text
        text_without_reaction = text[:-len(reaction_token)].strip()
        logging.warning(f"text_without_reaction:{text_without_reaction}")
        # Add the reaction to the message using the Slack API
        app.client.reactions_add(
            channel=channel,
            timestamp=ts,
            name=reaction_name,
        )
        # Return the message text without the reaction token
        return text_without_reaction
    else:
        # No reaction token found, return the original message text
        return text

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
    ts=message["ts"]
    message_text=message["text"]
    channel_id=message["channel"]
    chat_response = process_message(message_text, channel_id)
    chat_response = extract_and_add_reaction(chat_response,channel_id,ts)
    say(chat_response)

@app.event("app_mention")
def handle_app_mention_events(body, say):
    logger.debug("handle_app_mention_events")
    message_text = body["event"]["text"]
    channel_id = body["event"]["channel"]
    ts = body["event"]["ts"]
    chat_response = process_message(message_text, channel_id)
    chat_response = extract_and_add_reaction(chat_response,channel_id,ts)
    say(chat_response)

if __name__ == "__main__":
    SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()
    