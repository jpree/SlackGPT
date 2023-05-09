from langchain.chat_models import ChatOpenAI
from langchain.schema import AIMessage, HumanMessage, SystemMessage
from .config import PERSONA_TOKEN, logger
from typing import List
class ChatBot:
    def __init__(self, model_name, temperature):
        
        self._llm = ChatOpenAI(temperature=temperature, model_name=model_name,verbose=True)
    def get_prompt(self: str, prompt_file: str):
        with open(prompt_file, 'r') as file:
            # Read the content of the file into a string
            self._prompt = file.read()
        return self._prompt
    def chat(self, chat_history: List[str]):
        logger.info(chat_history)
        return self._llm(chat_history)    
    def get_ai_message(self, message: str):
        return AIMessage(content=message)
    def get_user_message(self, message: str):
        return HumanMessage(content=message)
    def get_system_message(self, message: str):
        return SystemMessage(content=message)