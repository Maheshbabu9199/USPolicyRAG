from src.utilities.logger import Logger
from fastapi.requests import Request
from src.utilities.constants import ConstantsRetriever
from src.router.dataclasses import UploadDocumentRequest, JsonDataDetails
from langchain_core.documents import Document
import os 
import json



logger = Logger.get_Logger(__name__)


class DocumentsHandler:


    def __init__(self):
        ...


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
            for file in fileslist[1:]:
                filepath = os.path.join(ConstantsRetriever.getConstants('data_dir')['folderpath'], file)
                jsondatalist = self.getJsonlist(filepath=filepath)
                complete_jsondata.extend(jsondatalist)
            
            chunks = []
            for json in complete_jsondata:
                json = self.parseJson(json)
                chunks.append(Document(content=json.rawtext, metadata={'document_identifier': json.identifier,
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
        try:

            # getting the list of files from the folder 
            fileslist = self.__getfiles(request.folderpath) 
            logger.critical(f"read files from the path: {request.folderpath}, total files {len(fileslist)}")

            # getting the list of jsons from the each file
            chunks = self.create_chunks(fileslist)
            return chunks 

        except Exception as exe:
            logger.error(f"error while processing json data: {exe}", exc_info=True)
            raise exe 