from chat_module.config import logger, DEFAULT_LANGUAGE_MODEL
from chat_module.chat_bot import ChatBot
from chat_module.slack_bot import SlackBot

def main():
    persona_ai = ChatBot(DEFAULT_LANGUAGE_MODEL, 0.9)
    classifier_ai = ChatBot("gpt-4", 0.9)
    slack_bot = SlackBot(persona_ai, classifier_ai)
    slack_bot.start()

if __name__ == "__main__":
    main()
