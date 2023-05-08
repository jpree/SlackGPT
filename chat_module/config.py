import os
import logging
from dotenv import load_dotenv

load_dotenv()

PERSONA_TOKEN = ";persona;"
DEFAULT_CHAT_HISTORY = 10
DEFAULT_LANGUAGE_MODEL = "gpt-3.5-turbo"
SLACK_BOT_TOKEN = os.environ.get("SLACK_BOT_TOKEN")
SLACK_APP_TOKEN = os.environ.get("SLACK_APP_TOKEN")
INCLUDED_CHAT_HISTORY = os.environ.get("INCLUDED_CHAT_HISTORY")
LANGUAGE_MODEL = os.environ.get("LANGUAGE_MODEL")

if INCLUDED_CHAT_HISTORY is not None:
    INCLUDED_CHAT_HISTORY = int(INCLUDED_CHAT_HISTORY)
else:
    INCLUDED_CHAT_HISTORY = DEFAULT_CHAT_HISTORY

if LANGUAGE_MODEL is not None:
    LANGUAGE_MODEL = str(LANGUAGE_MODEL)
else:
    LANGUAGE_MODEL = DEFAULT_LANGUAGE_MODEL

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
