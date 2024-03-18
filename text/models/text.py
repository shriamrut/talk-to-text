import datetime
from fastapi import File, UploadFile
from pydantic import BaseModel, Field
from typing_extensions import Annotated
from typing import Optional, List
from pydantic.functional_validators import BeforeValidator
from datetime import datetime

# Represents an ObjectId field in the database.
# It will be represented as a `str` on the model so that it can be serialized to JSON.
PyObjectId = Annotated[str, BeforeValidator(str)]

class Text(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    content: str = Field(title = "Content of the text", default = None)
    title: str = Field(title = "Title of the text", default = None)
    creationTimeStamp: datetime = Field(title = "Creation time stamp", default_factory=datetime.utcnow)

class TextResponse(BaseModel):
    id: Optional[PyObjectId] = Field(default=None, title="Id of the text")

class UploadText(BaseModel):
    file: UploadFile = File(...)
    title: str = Field(title = "Title of the text", default = None)
    chunkSize: int = Field(title = "Chunking of the text", default = 250)
    chunkOverlap: int = Field(title = "Chunk overlap of the text", default = 25)