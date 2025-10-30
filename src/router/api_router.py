from src.utilities.logger import Logger 
from fastapi import APIRouter
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from src.router.datamodels import LoadDataRequest, UploadDocumentRequest, QARequest
from src.services.documents_handler import DocumentsHandler
from src.services.service_handler import ServiceHandler
import time 

api_router = APIRouter()
logger = Logger.get_Logger(__name__)
documentshandler = DocumentsHandler()
servicehandler = ServiceHandler()


@api_router.post('/loadData')
def loadData(request: LoadDataRequest):
    """ 
    shows the data from the provided filepath
    """

    try:
        data = documentshandler.getData(request.filepath)         
        return JSONResponse(status_code=200, content={'message': data, 'status': 'Succesful'})
    
    except Exception as exec:
        logger.error(f"Error while loading the data from the path: {exec}", exc_info=True)
        return JSONResponse(status_code=500, content={'message': exec.__str__(), 'status': 'Unsuccesful'})
    

@api_router.post('/processData')
def getJsonList(request: LoadDataRequest):
    """ 
    gets the list of jsonDetails objects with selected fields only
    """
    try:
        data = documentshandler.getJsonlist(request.filepath) 
        return JSONResponse(content={'message': data, 'status': 'Succesful'}, status_code=200)

    except Exception as exec:
        logger.error(f"Error while uploading the data: {exec}", exc_info=True)
        return JSONResponse(content={'message': exec.__str__(), 'status': 'Unsuccessful'})
    


@api_router.post('/uploadData')
def uploadData(request:UploadDocumentRequest):
    """
    reads all the files in the folder, loads the data and uploads the info to the vector db, uploads only selected fields
    """
    try:
        result = documentshandler.processData(request)
        return JSONResponse(status_code=200, content={'status': 'Successful', 'message': result})

    except Exception as exec:
        logger.error(f"Error while uploading the data: {exec}", exc_info=True)
        return JSONResponse(content={'message': exec.__str__(), 'status': 'Unsuccessful'})



@api_router.post('/perform_QA')
def performQA(request: QARequest):
    try: 
        start_time = time.time()
        logger.info(f"starting Q&A for the user_id: {request.user_id}...")
        agent_response = servicehandler.performQA(request)

        return JSONResponse(
            content = {'result': agent_response, 
                       'message': 'Successful', 'process_time': time.time()-start_time},
            status_code = 200)

    except Exception as exec:
        logger.error(f"Error while performing Q&A: {exec}", exc_info=True)
        return JSONResponse(
            content = {'result': exec.__str__(), 
                       'message': 'UnSuccessful', 'process_time': time.time()-start_time},
            status_code = 500)