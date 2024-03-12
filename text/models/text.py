from pydantic import BaseModel, Field
from uuid import UUID

class Text(BaseModel):
    textId: UUID
    title: str
    text: str
    creationTimeStamp: str

class CreateText(BaseModel):
    text: str = Field(..., title = "Content of the text")
    title: str = Field(..., title = "Title of the text")