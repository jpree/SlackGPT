from chat_module.config import logger
from chat_module.chat_bot import ChatBot
from chat_module.slack_bot import SlackBot

def main():
    chatbot = ChatBot("gpt-3.5-turbo", 0.9)
    slack_bot = SlackBot(chatbot)
    slack_bot.start()

if __name__ == "__main__":
    main()
