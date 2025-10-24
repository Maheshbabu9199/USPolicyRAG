from sentence_transformers import SentenceTransformer
from src.utilities.logger import Logger


logger = Logger.get_Logger(__name__)


# from sentence_transformers import SentenceTransformer
# sentences = ["This is an example sentence", "Each sentence is converted"]

# model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
# embeddings = model.encode(sentences)
# print(embeddings)



class EmbeddingModel:

    def __init__(self,):
        self.model = SentenceTransformer(model='sentence-transformers/all-MiniLM-L6-v2', device='cuda', trust_remote_code=True)
        

    
    def embed(self, sentence:str):
        try:
            logger.info(f"embedding sentence {sentence}")
            embedding = self.model.encode(sentence)
            return embedding[0]
        
        except Exception as exec:
            logger.error(f"Error while embedding the sentence:{exec}", exc_info=True)
            raise exec 



    