from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema import HumanMessage

class GeminiLLMWrapper:
    def __init__(self, api_key, model="gemini-2.5-flash"):
        self.llm = ChatGoogleGenerativeAI(google_api_key=api_key, model=model)
    
    def generate(self, prompt):
        message = HumanMessage(content=prompt)
        response = self.llm.invoke([message])
        return response.content
