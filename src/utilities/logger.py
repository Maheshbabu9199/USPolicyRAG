from src.utilities.constants import ConstantsRetriever
from src.utilities.customsingleton import MySingleton
from logging import FileHandler, StreamHandler

import logging 
import os 




class Logger(MySingleton):

    @staticmethod
    def get_Logger(name:str):
        """
        logging configuration
        """

        logs_folder = os.path.join(os.getcwd(), 'logs')
        os.makedirs(logs_folder, exist_ok=True)
        filename = ConstantsRetriever.getConstants('logs_config')['logs_path']
        
        logging_format = "%(asctime)s : %(levelname)s : %(lineno)s : %(module)s : %(funcName)s : %(message)s"
        logging.basicConfig(format=logging_format, 
                            level=logging.INFO,
                            handlers=[FileHandler(filename=filename), StreamHandler()])


        logger = logging.getLogger(name)

        return logger 




        
        



        







        