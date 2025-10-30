from sentence_transformers import SentenceTransformer
from src.utilities.logger import Logger
import torch

logger = Logger.get_Logger(__name__)


# from sentence_transformers import SentenceTransformer
# sentences = ["This is an example sentence", "Each sentence is converted"]

# model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
# embeddings = model.encode(sentences)
# print(embeddings)



class EmbeddingModel:

    def __init__(self,):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model : SentenceTransformer = SentenceTransformer(model_name_or_path='sentence-transformers/all-MiniLM-L6-v2', 
                                                               device=self.device, trust_remote_code=True, )


    def batch_embeddings(self, texts:list[str]):
        """ 
        this is to embed the list of strings and return the embeddings in numpy array format

        args:
            texts (list[str]) : list of strings 
        
        returns:
            embeddings (np.array[arrays]): arrays of embeddings
        
        """
        try:
            logger.info(f"processing batch embeddgins")
            embeddings = self.model.encode(sentences=texts)
            logger.info(f'completed batch embeddings')
            return embeddings


        except Exception as exec:
            logger.error(f"error during batch embeddings: {exec}", exc_info=True)
            raise exec

    

    def encode_string(self, text:str):
        try:
            logger.info(f"Started embedding string: {text}")
            embedding = self.model.encode(text)
            return embedding


        except Exception as exec:
            logger.error(f"Error while embedding the string: {exec}", exc_info=True)
            raise exec 