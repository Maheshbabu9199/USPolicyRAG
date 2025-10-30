from src.utilities.logger import Logger
from src.utilities.constants import ConstantsRetriever
from src.utilities.customsingleton import MySingleton
from .llm_interface import LLMInterface
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from src.utilities.opik_config import OpikConfig
from dotenv import load_dotenv
import os 

load_dotenv()
logger = Logger.get_Logger(__name__)


class OpenAILLMs(MySingleton, LLMInterface):

    def __init__(self):
        self.opik_tracer = OpikConfig().OPIK_TRACER
        self.llm = ChatOpenAI(
            cache=True,
            verbose=True,
            callbacks=[],
            metadata={'service_provider': 'Openai'},
            model='gpt-4o-mini',
            api_key=os.getenv('OPENAI_API_KEY')
        )



    def generate_response(self):
        try:
            pass 


        except Exception as exec:
            logger.error(f"Error while generating llm response: {exec}", exc_info=True)
            raise exec
        

    
