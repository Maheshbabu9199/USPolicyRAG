from langchain_community.tools import DuckDuckGoSearchRun
from langchain.tools import tool


class LLMTools:

    @staticmethod
    @tool
    def websearch(query:str)-> str:
        """
        Search the web for current and factual information using DuckDuckGo.

        Use this tool when the user asks for **recent, factual, or real-time**
        information that may not exist in your local knowledge base — for example,
        current events, updated statistics, or policy changes.

        Args:
            query (str): The search query or question to look up online.

        Returns:
            str: A concise summary of the most relevant search results.
        
        """
        search = DuckDuckGoSearchRun()
        result = search.invoke(query)
        return result 
