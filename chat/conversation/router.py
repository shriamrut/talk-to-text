from typing import List
import uuid
from datetime import datetime
from uuid import UUID
from chat.models.conversation import Conversation, Message, CreateConversation, PostMessage
import logging
from inventory.client.conversation_collection import ConversationCollection
from fastapi.responses import Response
from fastapi import HTTPException, status, Body

from llm.service import LLMService
from text.service import TextService


class ConversationRouter:

    def __init__(self, app, tags):
        self.conversation_collection = ConversationCollection()
        self.llm_service = LLMService()
        self.text_service = TextService()
        
        @app.post("/v1/conversations/", tags = tags,
                  response_description = "Create new conversation",
                  response_model = Conversation,
                  status_code = status.HTTP_201_CREATED,
                  response_model_by_alias = False,)
        async def create_conversation(createConversation: CreateConversation = Body(...)):
            textId = createConversation.textId
            logging.info(f"Creating conversation on text with id {textId}")
            conversation = Conversation(messages = [], 
                                        textId = textId)
            conversation_from_db = self.conversation_collection.create_conversation(conversation)
            return conversation_from_db
        
        @app.post("/v1/conversations/{id}/messages", tags = tags,
                  response_description = "Adds new message to conversation and returns app response",
                  response_model = Message,
                  status_code = status.HTTP_202_ACCEPTED,
                  response_model_by_alias = False,)
        async def post_message(id: str, postMessage: PostMessage = Body(...)):
            logging.info(f"Got message from user: {postMessage.messageContent}")
        
            relevant_texts = self.text_service.get_relevant_texts(id, 
                                                                  postMessage.messageContent)
            generated_text = self.llm_service.query(relevant_texts=relevant_texts,
                                                    query=postMessage.messageContent)
            message = Message(messageContent = postMessage.messageContent,
                            isUser = True)
            response_message = Message(messageContent = generated_text,
                                       isUser = False)
            # Need to check if it returns true
            self.conversation_collection.add_message_to_conversation(message, id)
            self.conversation_collection.add_message_to_conversation(response_message, id)

            return response_message

        @app.get("/v1/conversations", tags = tags,
                 response_description = "Get all conversations",
                  response_model = List[Conversation],
                  response_model_by_alias = False,)
        def get_conversations() -> List[Conversation]:
            return self.conversation_collection.get_conversations()

        @app.get("/v1/conversations/{id}", tags = tags,
                 response_description = "Get a single conversation",
                 response_model = Conversation,
                 response_model_by_alias = False,)
        def get_conversation(id: str):
            conversation = self.conversation_collection.get_conversation(id)
            if conversation is not None:
                return conversation
            raise HTTPException(status_code=404, detail=f"Unable to find conversation with {id}")
        
        @app.delete("/v1/conversations/{id}", tags = tags, response_description = "Deletes a conversation")
        async def delete_conversation(id: str):
            delete_result = self.conversation_collection.delete_conversation(id)
            if delete_result.deleted_count == 1:
                return Response(status_code = status.HTTP_204_NO_CONTENT)
            raise HTTPException(status_code=500, detail=f"Unable to delete conversation with {id}")