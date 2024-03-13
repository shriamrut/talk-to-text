from pydantic import BaseModel, Field
from typing import List, Optional
from uuid import uuid4
from datetime import datetime
from typing_extensions import Annotated
from pydantic.functional_validators import BeforeValidator

# Represents an ObjectId field in the database.
# It will be represented as a `str` on the model so that it can be serialized to JSON.
PyObjectId = Annotated[str, BeforeValidator(str)]

class Message(BaseModel):
    messageId: Optional[PyObjectId] = Field(alias="_id", title = "Message Id", default=None)
    messageContent: str = Field(title = "Message content", default = "")
    creationTimeStamp: datetime = Field(title = "Creation time stamp", default_factory=datetime.utcnow)
    isUser: bool = Field(title = "Is the message sent by the user or not", default = None)

class Conversation(BaseModel):
    messages: List[Message]
    conversationId: Optional[PyObjectId] = Field(alias="_id", title = "Conversation Id", default=None)
    textId: Optional[PyObjectId] = Field(title = "Text Id associated with the conversation", default = None)
    creationTimeStamp: datetime = Field(title = "Creation time stamp", default_factory=datetime.utcnow)

class PostMessage(BaseModel):
    messageContent: str = Field(..., title = "Content of the message")

class CreateConversation(BaseModel):
    textId: Optional[PyObjectId] = Field(title = "Text Id")