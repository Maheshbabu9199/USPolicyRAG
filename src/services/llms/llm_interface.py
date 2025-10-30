from src.utilities.logger import Logger
from abc import ABC, abstractmethod


logger = Logger.get_Logger(__name__)


class LLMInterface(ABC):


    @abstractmethod
    def __init__():
        pass 

    @abstractmethod
    def generate_response():
        pass 

    # @abstractmethod
    # def getLLMDetails():
    #     pass 