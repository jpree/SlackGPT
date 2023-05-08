from langchain.chat_models import ChatOpenAI
from langchain.schema import AIMessage, HumanMessage, SystemMessage
from .config import PERSONA_TOKEN
from typing import List
class ChatBot:
    def __init__(self, model_name, temperature):
        # Open the file in read mode
        with open('persona_template.md', 'r') as file:
            # Read the content of the file into a string
            self._prompt_template = file.read()
        with open('default_template.md', 'r') as file:
            # Read the content of the file into a string
            self._default_template = file.read()
        self._llm = ChatOpenAI(temperature=temperature, model_name=model_name,verbose=True)
    def get_prompt(self, message):
        return self._prompt_template.replace(f"{PERSONA_TOKEN}", message)
    def get_default_prompt(self: str):
        return self._default_template
    def chat(self, chat_history: List[str]):
        return self._llm(chat_history)    
    def get_ai_message(self, message: str):
        return AIMessage(content=message)
    def get_user_message(self, message: str):
        return HumanMessage(content=message)
    def get_system_message(self, message: str):
        return SystemMessage(content=message)