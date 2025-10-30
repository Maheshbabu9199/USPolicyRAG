from qdrant_client import QdrantClient, models
from src.utilities.customsingleton import MySingleton
from src.services.llms.embedding import EmbeddingModel
from src.utilities.logger import Logger
from sentence_transformers import SentenceTransformer
from langchain_core.documents import Document
import uuid



logger = Logger.get_Logger(__name__)


class QdrantClientClass(MySingleton):


    def __init__(self):
        self.client = QdrantClient(url='http://localhost:6333')
        self.embedding_model : EmbeddingModel = EmbeddingModel()


    
    def uploadData(self, chunks: list[Document]):
        """ 
        uploads the data to the vectordb 

        """
        try:
            
            logger.info(f"started uploading data to vectordb process...")

            texts = [doc.page_content for doc in chunks]

            list_of_embeddings = self.embedding_model.batch_embeddings(texts=texts)

            result = self.client.upsert(
                collection_name='uspolicies',
                points = models.Batch(
                    ids = [uuid.uuid4().__str__() for i in range(len(texts))],
                    payloads=[
                        doc.metadata for doc in chunks
                    ],
                    vectors=list_of_embeddings
                ))


            if not result.status.value == 'completed':
                raise Exception('failed during upsert operation')

            return "Data Insertion Completed"

        except Exception as exec:
            logger.error(f"error while uploading data to vectordb process: {exec}", exc_info=True)
            raise exec

    

    def query_data(self, query:str):
        try:

            embedding = self.embedding_model.encode_string(query)
            logger.info(f"Starting vector search...")
            result_points = self.client.search(collection_name='uspolicies', query_vector=embedding,
                                            with_payload=True, with_vectors=False, limit=10)
            
            logger.info(f"Completed vector search....")
            
            return result_points


        except Exception as exec:
            logger.error(f"Error while querying data from vector database: {exec}", exc_info=True)
            raise exec




    