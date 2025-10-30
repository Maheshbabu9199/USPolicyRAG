from src.utilities.logger import Logger
from src.utilities.constants import ConstantsRetriever
from src.utilities.customsingleton import MySingleton
from langchain_core.documents import Document
from langchain_community.retrievers import BM25Retriever

logger = Logger.get_Logger(__name__)


class Retriever(MySingleton):


    def __init__(self, documents:list[Document]):
        self.retriever = BM25Retriever.from_documents(documents)
        self.retriever.k = 5


    def getRelevantDocuments(self, query:str=""):
        try:
            logger.info(f"Started getting relevant docs using BM25 Retriever...")
            documents = self.retriever.invoke(input=query)
            logger.info(f"Completed filtering using bm25 retriever...")
            return documents

        except Exception as exec:
            logger.error(f"Error while getting relevant documents: {exec}", exc_info=True)
            raise exec 