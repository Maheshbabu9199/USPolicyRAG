import os 
import yaml


class ConstantsRetriever:

    
    CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
    CONSTANTS_PATH = os.path.join(CURRENT_DIR, "../resources", "constants.yaml")
    with open(CONSTANTS_PATH, 'r') as f:
        constants = yaml.safe_load(f)

    @staticmethod
    def getConstants(constant_name:str):
        return ConstantsRetriever.constants[constant_name]