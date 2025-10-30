from src.utilities.logger import Logger
from src.utilities.customsingleton import MySingleton
from langchain_community.document_compressors import JinaRerank
from langchain_core.documents import Document
from dotenv import load_dotenv
import os 

load_dotenv()


logger = Logger.get_Logger(__name__)


class ReRanker(MySingleton):
    
    def __init__(self):
        self.reranker = JinaRerank(jina_api_key=os.getenv('JINAAI_APIKEY'))



    def reRankDocuments(self, docs:list[Document], query:str):
        try:
            logger.info(f"started ReRanking documents...")
            reranked_indexes = self.reranker.rerank(documents=docs, query=query, top_n=3)
            reranked_docs = [docs[res['index']] for res in reranked_indexes]
            logger.info(f"completed reranking docs...")
            return reranked_docs
        
        except Exception as exc:
            logger.error(f"Error while reranking documents: {exc}", exc_info=True)
            raise exc

