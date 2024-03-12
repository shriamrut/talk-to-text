from pydantic import BaseModel, Field
from typing import List
import uuid
from uuid import UUID
from datetime import datetime

class Message(BaseModel):
    messageId: str = Field(default_factory=uuid.uuid4, alias="_id")
    messageContent: str
    creationTimeStamp: datetime = Field(default_factory=datetime.utcnow)
    isUser: bool

class Conversation(BaseModel):
    messages: List[Message]
    conversationId: str = Field(default_factory=uuid.uuid4, alias="_id")
    textId: str = Field(default_factory=uuid.uuid4)
    creationTimeStamp: datetime = Field(default_factory=datetime.utcnow)


class PostMessage(BaseModel):
    messageContent: str = Field(..., title = "Content of the message")

class CreateConversation(BaseModel):
    textId: str  = Field(..., title = "Text ID")