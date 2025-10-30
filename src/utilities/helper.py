from .logger import Logger
from .customsingleton import MySingleton
from langchain_core.documents import Document
from qdrant_client import models
logger = Logger.get_Logger(__name__)


class Helper(MySingleton):


    @staticmethod
    def convert_to_Documents_from_StructPoints(points:list[models.ScoredPoint]):
        try:
            logger.info(f"Converting from Structpoints to Documents")
            documents = []
            for point in points:
                payload = point.payload
                doc = Document(
                    page_content=payload.get("raw_text", ""),  # main bill text
                    metadata={
                        "id": point.id,
                        "score": point.score,
                        "document_identifier": payload.get("document_identifier"),
                        "year": payload.get("year"),
                        "title": payload.get("title"),
                        "actions": payload.get("actions"),
                        "sponsors": payload.get("sponsors"),
                        "subject": payload.get("subject"),
                    }
                )
                documents.append(doc)
            
            return documents 

        except Exception as exc:
            logger.error(f"Error while converting structpoints to Documents: {exc}", exc_info=True)
            raise exc
    

    @staticmethod
    def build_context(docs):
        try:

            context_parts = []
            for doc in docs:
                meta = doc.metadata
                summary = f"""
                ### {meta.get('document_identifier', 'Unknown ID')} ({meta.get('year', 'N/A')}):
                Title: {meta.get('title')}
                Subject: {', '.join(meta.get('subject', []))}
                Key Actions: {[a['description'] for a in meta.get('actions', []) if 'description' in a]}
                Sponsors: {[s['name'] for s in meta.get('sponsors', []) if 'name' in s]}
                Snippet Summary : {doc.page_content[:400]}...
                """
                context_parts.append(summary.strip())
            return "\n\n".join(context_parts)
        

        except Exception as exc:
            logger.error(f"Error while formatting context: {exc}", exc_info=True)
            raise exec