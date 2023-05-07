from langchain.chat_models import ChatOpenAI
from langchain.schema import AIMessage, HumanMessage, SystemMessage
class ChatBot:
    def __init__(self, model_name, temperature):
        # Open the file in read mode
        with open('persona_template.md', 'r') as file:
            # Read the content of the file into a string
            self._prompt_template = file.read()
        self._llm = ChatOpenAI(temperature=temperature, model_name=model_name,verbose=True)

    def get_prompt(self, message):
        return self._prompt_template.replace("<persona>", message)
    def chat(self, messages):
        return self._llm(messages)    
    def get_ai_message(self, message):
        return AIMessage(content=message)
    def get_user_message(self, message):
        return HumanMessage(content=message)
    def get_system_message(self, message):
        return SystemMessage(content=message)