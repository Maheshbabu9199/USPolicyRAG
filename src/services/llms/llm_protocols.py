from typing import Protocol



class LLMProtocol(Protocol):


    def __init__(self):
        ...


    def generate_response(self):
        ...


    