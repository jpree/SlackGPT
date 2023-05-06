import os
import sys
import logging
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from argparse import ArgumentParser
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQAWithSourcesChain

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Initialize the Slack app
def initialize_app():
    return App(token=os.environ.get("SLACK_BOT_TOKEN"))

# Initialize the Slack app
app = initialize_app()

# Initialize the conversational retrieval chain
def initialize_chain():
    embeddings = OpenAIEmbeddings()
    vec_search = Chroma(embedding_function=embeddings, persist_directory=".coupa")

    return RetrievalQAWithSourcesChain.from_chain_type(
        ChatOpenAI(
            temperature=0.9,
            model_name="gpt-3.5-turbo",#"gpt-4",#gpt-3.5-turbo",
            verbose=True
        ),
        chain_type="stuff",
        retriever=vec_search.as_retriever(k=5)
    )

# Process a message using the conversational retrieval chain
def process_message(chain, message_text):
    try:
        resp = chain({"question":message_text}, return_only_outputs=True)
        return resp["answer"]
    except Exception as e:
        logger.error(f"Error processing message: {e}")
        return "Sorry, something went wrong. Please try again later."

# Handle incoming messages that mention the bot
@app.message(".*")
def handle_mention(message, say, logger):
    # Validate the message
    if not message or "text" not in message or not message["text"]:
        logger.warning("Invalid or empty message received")
        return

    # Log the message at DEBUG level
    logger.debug(message)
    message_text = message["text"]
    response = process_message(chain, message_text)
    say(response)

# Handle app_mention events
@app.event("app_mention")
def handle_app_mention_events(body, say, logger):
    # Validate the event
    if not body or "event" not in body or "text" not in body["event"] or not body["event"]["text"]:
        logger.warning("Invalid or empty event received")
        return

    # Log the event at DEBUG level
    logger.debug(body)
    message_text = body["event"]["text"]
    response = process_message(chain, message_text)
    say(response)

# Main entry point
if __name__ == "__main__":
    chain = initialize_chain()
    SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()
