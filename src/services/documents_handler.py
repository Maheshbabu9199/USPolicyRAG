from src.utilities.logger import Logger
from fastapi.requests import Request
from src.utilities.constants import ConstantsRetriever
from src.router.datamodels import UploadDocumentRequest, JsonDataDetails
from src.utilities.qdrant_vectordb import QdrantClientClass
from langchain_core.documents import Document
import os 
import json



logger = Logger.get_Logger(__name__)


class DocumentsHandler:


    def __init__(self):
        self.vectordb = QdrantClientClass()


    def getData(self, filepath:str):

        """ 
        loads and returns the data from the provided filepath

        args:
            filepath (str) : path of the file to be read

        returns: 
            data (str): data from the file
        """
        try:
            with open(filepath, 'r') as f:
                data = json.load(f)
            return data


        except Exception as exec:
            logger.error(f"error while loading the data: {exec}", exc_info=True)
            raise exec

    def parseJson(self, data:dict):
        try:
            jsondata = JsonDataDetails(rawtext=data['raw_text'],
                                    year=int(data['legislative_session'][:-2]) or 2025,
                                    identifier = data['identifier'],
                                    title = data['title'],
                                    actions = data['actions'],
                                    subject = data['subject']  or None,
                                    sponsers = data['sponsors'])

            logger.debug(f"json data parsed: {jsondata}")
            return jsondata

        except Exception as exec:
            logger.error(f"error while parsing doc: {exec}", exc_info=True)
            raise exec
        
    
    def getJsonlist(self, filepath:str):
        """
        this is to parse the data from the file and return the only required info.
        """
        try:
            data = self.getData(filepath=filepath)
            json_details = []
            for d in data:
                d_result = self.parseJson(d)
                json_details.append(d)

            return json_details

        except Exception as exec:
            logger.error(f"error while getting json data list: {exec}", exc_info=True)
            raise exec 



    def __getfiles(self, folderpath:str)-> list:
        try:
            files = os.listdir(folderpath)
            return files 
        

        except Exception as exec:
            logger.error(f"error while reading files from the folderpath: {exec}", exc_info= True)
            raise exec 


    def create_chunks(self, fileslist:list):
        """ 
        create list of Documents from the list of jsons data

        args:
            jsonlist (list) : contains list of json data

        returns:
            chunks (list[Document]) : list of documents
        
        """

        try:
            logger.info(f"started creating chunks...")
            complete_jsondata = [] 
            for file in fileslist:
                filepath = os.path.join(ConstantsRetriever.getConstants('data_dir')['folderpath'], file)
                jsondatalist = self.getJsonlist(filepath=filepath)
                complete_jsondata.extend(jsondatalist)
            
            chunks = []
            for json in complete_jsondata:
                json = self.parseJson(json)
                chunks.append(Document(page_content=json.rawtext, metadata={'document_identifier': json.identifier,
                                                                        'year': json.year,
                                                                        'title': json.title,
                                                                        'actions': json.actions,
                                                                        'sponsors': json.sponsers,
                                                                        'subject': json.subject,
                                                                        'raw_text': json.rawtext
                                                                        }))
                
            return chunks

        except Exception as exec:
            logger.error(f"error while creating chunks: {exec}", exc_info=True)
            raise exec 




    def processData(self, request:UploadDocumentRequest):
        """ 
        from the folderpath, reads the files, gets the data and vectorizes the selected fields to the vectordb

        args:
            request (UploadDocumentRequest) : request

        returns:
            upload_status (str) : successful message
        
        """
        try:

            # getting the list of files from the folder 
            fileslist : list[str] = self.__getfiles(request.folderpath) 
            logger.critical(f"read files from the path: {request.folderpath}, total files {len(fileslist)}")

            # getting the list of jsons from the each file
            chunks : list[Document] = self.create_chunks(fileslist)
            
            # upload to vectordb
            upload_status = self.vectordb.uploadData(chunks)
            
            return upload_status

        except Exception as exe:
            logger.error(f"error while processing json data: {exe}", exc_info=True)
            raise exe 