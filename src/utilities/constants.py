import os 
import yaml


class ConstantsRetriever:

    
    with open("/home/user/Projects/USPolicyRAG/src/resources/constants.yaml", 'r') as f:
        constants = yaml.safe_load(f)

    @staticmethod
    def getConstants(constant_name:str):
        return ConstantsRetriever.constants[constant_name]