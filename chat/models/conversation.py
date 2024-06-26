from pydantic import BaseModel, Field
from typing import List, Optional
from uuid import uuid4
from datetime import datetime
from typing_extensions import Annotated
from pydantic.functional_validators import BeforeValidator
from bson import ObjectId

# Represents an ObjectId field in the database.
# It will be represented as a `str` on the model so that it can be serialized to JSON.
PyObjectId = Annotated[str, BeforeValidator(str)]

class Message(BaseModel):
    messageId: Optional[PyObjectId] = Field(alias="_id", default_factory = lambda: str(ObjectId()), title = "Message Id")
    messageContent: str = Field(title = "Message content", default = "")
    creationTimeStamp: datetime = Field(title = "Creation time stamp", default_factory=datetime.utcnow)
    isUser: bool = Field(title = "Is the message sent by the user or not", default = None)

class Conversation(BaseModel):
    messages: List[Message]
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    textId: Optional[PyObjectId] = Field(title = "Text Id associated with the conversation", default = None)
    creationTimeStamp: datetime = Field(title = "Creation time stamp", default_factory=datetime.utcnow)

class PostMessage(BaseModel):
    messageContent: str = Field(..., title = "Content of the message")
    referenceChunkCount: int = Field(default = 7, title = "Number of reference chunks to be considered for RAG")

class CreateConversation(BaseModel):
    textId: Optional[PyObjectId] = Field(title = "Text Id")