import os
import sys
import logging
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from argparse import ArgumentParser
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory

# Initializes your app with your bot token and signing secret
app = App(
    token=os.environ.get("SLACK_BOT_TOKEN")
)

# Initialize embeddings, Chroma vector store, and conversation memory
embeddings = OpenAIEmbeddings()
vec_search = Chroma(embedding_function=embeddings, persist_directory=".coupa")
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

# Initialize the conversational retrieval chain
chain = ConversationalRetrievalChain.from_llm(
    llm=ChatOpenAI(
        temperature=0.9,
        model_name="gpt-3.5-turbo",
        verbose=True
    ),
    chain_type="stuff",
    retriever=vec_search.as_retriever(),
    memory=memory
)

# Define a function to handle incoming messages that mention the bot
@app.message(".*")
def handle_mention(message, say, logger):
    print(message)
    
    # Get the text of the incoming message
    message_text = message["text"]
    #llm = get_chatai()
    resp = chain.run(message_text)#({"question": message_text})
    say(resp)

@app.event("app_mention")
def handle_app_mention_events(body, say, logger):
    print(body)

    message_text = body["event"]["text"]
    #llm = get_chatai()
    resp = chain.run(message_text)
    say(resp)
    
# Start your app
if __name__ == "__main__":
    SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()


