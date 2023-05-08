import re
from typing import List
from slack_sdk.errors import SlackApiError
from .config import logger, PERSONA_TOKEN, INCLUDED_CHAT_HISTORY
from .chat_bot import ChatBot

def get_purpose(chatbot: ChatBot, app, channel_id: str, bot_user_id: str) -> str:
    try:
        logger.info("Fetching channel purpose for channel ID: %s", channel_id)
        channel_purpose = chatbot.get_default_prompt()
        # Call the conversations.info method using the WebClient
        # Requires "channels:read" and "groups:read" permissions
        response = app.client.conversations_info(channel=channel_id)
        # Check if the API call was successful
        if response['ok']:
            logger.info("Detected channel persona")
            # Check if the 'purpose' key exists in the response dictionary
            if 'purpose' in response['channel']:
                logger.info(f"{PERSONA_TOKEN} - {response['channel']['purpose']['value']}")
                if response['channel']['purpose']['value'].startswith(f"{PERSONA_TOKEN}"):
                    logger.info("Adding persona to template")
                    channel_purpose = response['channel']['purpose']['value'][len(f"{PERSONA_TOKEN}"):]
                    channel_purpose=chatbot.get_prompt(channel_purpose)
                    logger.debug(f"FINAL:{channel_purpose}")
    except Exception as e:
        logger.error("Error in get_purpose", exc_info=1)
    return(channel_purpose.replace(f"{bot_user_id}", bot_user_id))

def get_chat_history(chatbot: ChatBot, app, channel_id: str, bot_user_id: str) -> List[str]:
    try:
        logger.info("Fetching chat history for channel ID: %s", channel_id)
        # Call the conversations_history method using the WebClient
        # Requires "channels:history", "groups:history", "im:history", and "mpim:history" permissions
        response = app.client.conversations_history(channel=channel_id, limit=INCLUDED_CHAT_HISTORY)
    except SlackApiError as e:
        logger.error(f"Error fetching chat history: {e}")
        return []

    prompt=get_purpose(chatbot, app, channel_id, bot_user_id)
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

def extract_and_add_reaction(app, text: str, channel: str, ts: str) -> str:
    logger.info("Extracting and adding reaction: channel ID: %s, ts: %s", channel, ts)
    # Search for the reaction token using a regular expression
    match = re.search(r'\[(\w+)\]$', text)
    if match:
        reaction_token = match.group(0)
        # Remove the delimiter characters from the reaction token
        reaction_name = reaction_token[1:-1]
        # Remove the reaction token from the message text
        text_without_reaction = text[:-len(reaction_token)].strip()
        logger.warning(f"text_without_reaction:{text_without_reaction}")
        # Add the reaction to the message using the Slack API
        # Call the reactions_add method using the WebClient
        # Requires "reactions:write" permission
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

def process_message(chatbot: ChatBot, app, message_text: str, channel_id: str, bot_user_id: str) -> str:
    try:
        logger.info("Processing message: message_text: %s, channel ID: %s", message_text, channel_id)
        chat_history = get_chat_history(chatbot, app, channel_id, bot_user_id)
        response = chatbot.chat(chat_history)
        return response.content
    except Exception as e:
        logger.error(f"Error processing message: {e}")
        return "Sorry, something went wrong. Please try again later."
