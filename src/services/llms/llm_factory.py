from src.utilities.customsingleton import MySingleton
from src.utilities.logger import Logger
from src.utilities.constants import ConstantsRetriever
from .openai_llms import OpenAILLMs
from .groq_llms import GroqLLMs
from .llm_interface import LLMInterface
import os 



class LLMFactory(MySingleton):

    __llms_details = {
        "openai": OpenAILLMs(),
        "groq": GroqLLMs()
    }

    @classmethod
    def getLLM(cls, objective:str='query_llm') -> LLMInterface:
        """
        initiates the llm instance based on the objective and returns the instance

        """

        if objective=='query_llm':
            return LLMFactory.__llms_details.get(ConstantsRetriever.getConstants('llms_config')['query_rewritellm_serviceprovider'], 'openai')
        else:
            return LLMFactory.__llms_details.get(ConstantsRetriever.getConstants('llms_config')['answer_llm_serviceprovider'], 'openai')

        

