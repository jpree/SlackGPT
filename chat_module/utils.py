import re
from typing import List
import json
from slack_sdk.errors import SlackApiError
from .config import logger, PERSONA_TOKEN, INCLUDED_CHAT_HISTORY
from .chat_bot import ChatBot

# Get's the prompt and does replacements
def get_purpose(chatbot: ChatBot, app, channel_id: str, bot_user_id: str, prompt_file: str) -> str:
    try:
        logger.info("Fetching channel purpose for channel ID: %s", channel_id)

        prompt = chatbot.get_prompt(prompt_file)
        channel_type = "unknown"
        channel_privacy_type = "unknown"
        channel_name = "unknown"
        channel_topic = "unknown"
        channel_purpose = "unknown"       

        # Call the conversations.info method using the WebClient
        # Requires "channels:read" and "groups:read" permissions
        response = app.client.conversations_info(channel=channel_id)
        # Check if the API call was successful
        if response['ok']:
            if 'is_channel' in response['channel'] and response['channel']['is_channel']:
                channel_type = "channel"

                if 'is_private' in response['channel'] and response['channel']['is_private']:
                    channel_privacy_type = "private"
                else:
                    channel_privacy_type = "public"
            elif 'is_group' in response['channel'] and response['channel']['is_group']:
                channel_type = "group"
            elif 'is_im' in response['channel'] and response['channel']['is_im']:
                channel_type = "im"

            if 'name' in response['channel']:
                channel_name = response['channel']['name']

            if 'purpose' in response['channel']:
                channel_purpose = response['channel']['purpose']['value']

            if 'topic' in response['channel']:
                channel_topic = response['channel']['topic']['value']

        members = get_participants(app, channel_id=channel_id)

        prompt = prompt.replace("{CHANNEL_USERS}", json.dumps(members)[1:-1])
        prompt = prompt.replace("{CHANNEL_NAME}", json.dumps(channel_name)[1:-1])
        prompt = prompt.replace("{CHANNEL_TYPE}", json.dumps(channel_type)[1:-1])
        prompt = prompt.replace("{CHANNEL_PRIVACY}", json.dumps(channel_privacy_type)[1:-1])
        prompt = prompt.replace("{CHANNEL_TOPIC}", json.dumps(channel_topic)[1:-1])
        prompt = prompt.replace("{CHANNEL_PURPOSE}", json.dumps(channel_purpose)[1:-1])
        prompt = prompt.replace("{BOT_USER_ID}", bot_user_id)
        logger.debug(prompt)
    except Exception as e:
        logger.error("Error in get_purpose", exc_info=1)
    return prompt


def get_chat_history(chatbot: ChatBot, app, channel_id: str, bot_user_id: str, prompt: str) -> List[str]:
    try:
        logger.info("Fetching chat history for channel ID: %s", channel_id)
        # Call the conversations_history method using the WebClient
        # Requires "channels:history", "groups:history", "im:history", and "mpim:history" permissions
        response = app.client.conversations_history(channel=channel_id, limit=INCLUDED_CHAT_HISTORY)
    except SlackApiError as e:
        logger.error(f"Error fetching chat history: {e}")
        return []

    
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

def react_message(app, channel: str, timestamp: str, emote: str) -> None:
    logger.info("Adding reaction to message: channel ID: %s, timestamp: %s, emote: %s", channel, timestamp, emote)
    # Call the reactions_add method using the WebClient
    # Requires "reactions:write" permission
    app.client.reactions_add(
        channel=channel,
        timestamp=timestamp,
        name=emote)

def process_message(persona_ai: ChatBot, classifier_ai: ChatBot, app, message_text: str, channel_id: str, bot_user_id: str) -> str:
    try:
        logger.info("Invoking classifier: channel ID: %s", channel_id)
        prompt = get_purpose(persona_ai, app, channel_id, bot_user_id, "classifier.txt")
        chat_history = get_chat_history(persona_ai, app, channel_id, bot_user_id, prompt)
        response = classifier_ai.chat(chat_history).content
        #logger.info(response)
        content=""
        if "<IGNORE>" in response:
            logger.info("Ignored")
            logger.debug(response)
        else:
            logger.info("Invoking Persona: channel ID: %s", channel_id)
            prompt = get_purpose(persona_ai, app, channel_id, bot_user_id, "persona.txt")
            chat_history = get_chat_history(persona_ai, app, channel_id, bot_user_id, prompt)
            content = persona_ai.chat(chat_history).content

        return content
    except Exception as e:
        logger.error(f"Error processing message: {e}")
        return "Sorry, something went wrong. Please try again later."
    
def get_participants(app, channel_id):
    try:
        # Get the list of members in the conversation
        result = app.client.conversations_members(channel=channel_id)
        member_ids = result["members"]

        # Get user info for each member
        members = []
        for member_id in member_ids:
            user_info = app.client.users_info(user=member_id)
            user = user_info["user"]

            # Extract the required fields and create a new dictionary for the user
            user_data = {
                "id": user["id"],
                "name": user["name"],
                "deleted": user["deleted"],
                "real_name": user["real_name"],
                "tz": user["tz"],
                "tz_label": user["tz_label"],
                "is_bot": user["is_bot"],
                "title": user["profile"].get("title", "")
            }
            members.append(user_data)

        return members
    
    except SlackApiError as e:
        logger.error(f"Error: {e}")
        return "Sorry, something went wrong. Please try again later."
