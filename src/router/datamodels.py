from pydantic import BaseModel, Field 
from typing import Union



# Request formats 

class LoadDataRequest(BaseModel):
    """
    this is for creating loaddata request
    """
    filepath: str = Field(..., example='filepath')


class UploadDocumentRequest(BaseModel):
    """ 
    this is for creating uploaddocument request
    """
    folderpath: str = Field(..., example='folderpath')


class QARequest(BaseModel):
    """
    for creating QA request
    """
    user_id: int = Field(..., example=123)
    query: str = Field(..., example="What is HB 8 from Alabama about?")
    

# JsonData format

class JsonDataDetails(BaseModel):
    """
    this class is for creating pydantic data class of selected fields from the json data
    """
    rawtext: str = Field(..., example='this is raw text')
    year: int = Field(..., example='2025')
    identifier : str = Field(..., example='HB 8')
    title : str = Field(..., example='title of the bill')
    actions : Union[list[dict], None] = Field(..., example=[{}])
    sponsers : Union[list[dict], None] = Field(..., example = [{}])
    subject: Union[list | None] = Field(..., example=[{}])


