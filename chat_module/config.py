import os
import logging
from dotenv import load_dotenv

load_dotenv()

PERSONA_TOKEN = ";persona;"
INCLUDED_CHAT_HISTORY = 1
SLACK_BOT_TOKEN = os.environ.get("SLACK_BOT_TOKEN")
SLACK_APP_TOKEN = os.environ.get("SLACK_APP_TOKEN")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
