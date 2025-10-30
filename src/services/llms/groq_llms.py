from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain.agents import create_agent
from src.utilities.logger import Logger
from src.utilities.customsingleton import MySingleton
from .llm_interface import LLMInterface
from src.utilities.opik_config import OpikConfig
from src.services.llms.llm_tools import  LLMTools
from dotenv import load_dotenv
import os 

load_dotenv()
logger = Logger.get_Logger(__name__)


class GroqLLMs(MySingleton, LLMInterface):
    
    def __init__(self):
        self.llm = ChatGroq(name='groq_llm',  verbose=True,
                              metadata={'service_provider': 'Groq'}, model='openai/gpt-oss-120b', api_key=os.getenv('GROQ_API_KEY'),
                              callbacks=[OpikConfig.OPIK_TRACER])
        
        self.agent = create_agent(model=self.llm, tools=[LLMTools.websearch], system_prompt=OpikConfig.getPrompt(promptName='USPolicies_Agent_SystemPrompt').prompt)


    def generate_response(self, template:ChatPromptTemplate, user_query: str, format_instructions:str):
        """
        generates response from the query
        """

        try:

            formatted_prompt = template.format_messages(user_query=user_query, format_instructions=format_instructions)
            response = self.llm.invoke(formatted_prompt)
            return response.content
            


        except Exception as exec:
            logger.error(f"Error while generating response from llm:{exec}",exc_info=True)
            raise exec 
        


    def getResponseFromAgent(self, user_input):
        try:
            logger.info(f"Started generating response from agent...")
            inputs = {'messages': [{'role': 'user', 'content': user_input}]}
            agent_response = self.agent.invoke(input=inputs)

            return agent_response['messages'][-1].content

        except Exception as exec:
            logger.error(f"Error while generating response from agent: {exec}", exc_info=True)
            raise exec 