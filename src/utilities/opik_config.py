from .logger import Logger
from .customsingleton import MySingleton
from opik import Opik, configure
from dotenv import load_dotenv
from opik.integrations.langchain import OpikTracer
import os 

logger = Logger.get_Logger(__name__)
configure(api_key=os.getenv('OPIK_API_KEY'), use_local=False)

class OpikConfig(MySingleton):

    # for logs tracking
    OPIK_TRACER = OpikTracer(project_name='USPoliciesRAG') 
    opik = Opik(project_name='USPoliciesRAG', api_key=os.getenv('OPIK_API_KEY'))


    @classmethod
    def getPrompt(cls, promptName: str):
        try:
            promptObj = cls.opik.get_prompt(name=promptName)
            return promptObj


        except Exception as exec:
            logger.error(f"Error while fetching prompt")
            raise exec