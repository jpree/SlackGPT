import pytest
from chat_module.chat_bot import ChatBot

@pytest.fixture
def chatbot():
    return ChatBot("gpt-3.5-turbo", 0.9)
