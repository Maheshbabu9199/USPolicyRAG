from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.documents import Document
from qdrant_client import models
from src.router.datamodels import QARequest
from src.services.llms.output_formats import RewriteOutputFormat
from src.services.retrievers import Retriever
from src.services.reranker import ReRanker
from src.utilities.logger import Logger
from src.utilities.customsingleton import MySingleton
from src.utilities.opik_config import OpikConfig
from src.utilities.qdrant_vectordb import QdrantClientClass
from src.utilities.helper import Helper
from .llms.llm_factory import LLMFactory
from .llms.llm_protocols import LLMProtocol
import json



logger = Logger.get_Logger(__name__)


class ServiceHandler(MySingleton):

    def __init__(self):
        self.rewrite_llm = LLMFactory.getLLM(objective='query_llm')
        self.answer_llm = LLMFactory.getLLM(objective='answer_llm')
        # self.opik = OpikConfig()
        self.rewrite_outputparser = PydanticOutputParser(pydantic_object=RewriteOutputFormat)
        self.vectordb = QdrantClientClass()
        self.reranker = ReRanker()

    def rewriteUserInput(self, user_query:str):
        try:
            logger.info(f"Started rewriting user query...")
            
            promptObj = OpikConfig.getPrompt(promptName='USPoliciesRAG_Rewrite_Prompt')
            format_instructions = self.rewrite_outputparser.get_format_instructions()
            user_prompt = """
                Here is the input query from the user:
                **Input Query:** {user_query}

                Rewrite the prompt based on the context in the following format:
                {format_instructions}
                """
            
            prompt = ChatPromptTemplate.from_messages([
                'system', promptObj.prompt,
                'human', user_prompt
            ])

            response =  self.rewrite_llm.generate_response(template=prompt, user_query=user_query, format_instructions=json.dumps(format_instructions))
            rewritten_query = self.rewrite_outputparser.parse(response)
            return rewritten_query

        except Exception as exec:
            logger.error(f"error while rewriting user query: {exec}", exc_info=True)
            raise exec
        

    def getAgentResponse(self, user_query:str, reranked_docs:list[Document]):
        try:
            promptObj = OpikConfig.getPrompt(promptName='USPolicies_Agent_UserPrompt')
            user_prompt = promptObj.format(user_query=user_query, retrieved_context=Helper.build_context(reranked_docs))

            agent_response = self.rewrite_llm.getResponseFromAgent(user_prompt)
            logger.info(f"Completed AGENT RESPONSE...")
            return agent_response


        except Exception as exec:
            logger.error(f"Error while getting final agent response: {exec}", exc_info=True)
            raise exec

    def performQA(self, request: QARequest):
        try:
            
            # rewriting the user query
            rewritten_query = self.rewriteUserInput(request.query)

            # performing vector search
            points : list[models.ScoredPoint]= self.vectordb.query_data(query=rewritten_query.rewritten_query)
            documents : list[Document] = Helper.convert_to_Documents_from_StructPoints(points)

            # performing sparse search 
            retriever = Retriever(documents=documents)
            filtered_documents: list[Document] = retriever.getRelevantDocuments(rewritten_query.rewritten_query)

            # re-ranking the filtered docs
            reranked_docs: list[Document]= self.reranker.reRankDocuments(docs=filtered_documents, query=rewritten_query.rewritten_query)
            
            agent_response = self.getAgentResponse(user_query=rewritten_query.rewritten_query, reranked_docs=reranked_docs)

            return agent_response
            

        except Exception as exec:
            logger.error(f"Error while performing QA: {exec}", exc_info=True)
            raise exec
    
