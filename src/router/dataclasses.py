from pydantic import BaseModel, Field 
from typing import Union

class LoadDataRequest(BaseModel):
    filepath: str = Field(..., example='filepath')


class JsonDataDetails(BaseModel):
    rawtext: str
    year: int
    identifier : str
    title : str
    actions : Union[list[dict], None]
    sponsers : Union[list[dict], None]
    subject: Union[list | None]


class UploadDocumentRequest(BaseModel):

    folderpath: str = Field(..., example='folderpath')

