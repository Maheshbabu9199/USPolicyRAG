from src.utilities.logger import Logger 
from fastapi import APIRouter
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from src.router.dataclasses import LoadDataRequest, JsonDataDetails, UploadDocumentRequest
from src.services.documents_handler import DocumentsHandler


api_router = APIRouter()
logger = Logger.get_Logger(__name__)
documentshandler = DocumentsHandler()


@api_router.post('/load_data')
def load_data(request: LoadDataRequest):
    try:
        data = documentshandler.getData(request.filepath)         
        return JSONResponse(status_code=200, content={'message': data, 'status': 'Succesful'})
    
    except Exception as exec:
        logger.error(f"Error while loading the data from the path: {exec}", exc_info=True)
        return JSONResponse(status_code=500, content={'message': exec.__str__(), 'status': 'Unsuccesful'})
    

@api_router.post('/processdata')
def getJsonList(request: LoadDataRequest):
    try:
        data = documentshandler.getJsonlist(request.filepath) 
        return JSONResponse(content={'message': 'done', 'status': 'Succesful'}, status_code=200)

    except Exception as exec:
        logger.error(f"Error while uploading the data: {exec}", exc_info=True)
        return JSONResponse(content={'message': exec.__str__(), 'status': 'Unsuccessful'})
    


@api_router.post('/uploadData')
def uploadData(request:UploadDocumentRequest):
    try:
        result = documentshandler.processData(request)
        return JSONResponse(status_code=200, content={'status': 'Successful', 'message': result})

    except Exception as exec:
        logger.error(f"Error while uploading the data: {exec}", exc_info=True)
        return JSONResponse(content={'message': exec.__str__(), 'status': 'Unsuccessful'})
