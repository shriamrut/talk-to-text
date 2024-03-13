from typing import List
import uuid
from datetime import datetime
from uuid import UUID
from chat.models.conversation import Conversation, Message, CreateConversation, PostMessage
import logging
from inventory.conversation_inventory_client import ConversationInventoryClient
from fastapi.responses import Response
from fastapi import HTTPException, status, Body


class ConversationController:

    def __init__(self, app, tags):
        self.conversations_inventory_client = ConversationInventoryClient()
        @app.post("/v1/conversations/", tags = tags,
                  response_description = "Create new conversation",
                  response_model = Conversation,
                  status_code = status.HTTP_201_CREATED,
                  response_model_by_alias = False,)
        async def create_conversation(createConversation: CreateConversation = Body(...)):
            textId = createConversation.textId
            logging.debug(f"Creating conversation on text with id {textId}")
            conversation = Conversation(messages = [], 
                                        textId = textId)
            conversation_from_db = self.conversations_inventory_client.create_conversation(conversation)
            return conversation_from_db
        
        @app.post("/v1/conversations/{conversationId}/messages", tags = tags,
                  response_description = "Adds new message to conversation and returns app response",
                  response_model = Message,
                  status_code = status.HTTP_202_ACCEPTED,
                  response_model_by_alias = False,)
        async def post_message(conversationId: str, postMessage: PostMessage = Body(...)):
            logging.debug(f"Got message from user: {postMessage.messageContent}")
            message = Message(messageContent = postMessage.messageContent,
                            isUser = True)
            response_message = Message(messageContent = "Hi, in WIP!",
                                       isUser = False)
            # Need to check if it returns true
            self.conversations_inventory_client.post_message_to_conversation(message, conversationId)
            self.conversations_inventory_client.post_message_to_conversation(response_message, conversationId)

            return response_message

        @app.get("/v1/conversations", tags = tags,
                 response_description = "Get all conversations",
                  response_model = List[Conversation],
                  response_model_by_alias = False,)
        def get_conversations() -> List[Conversation]:
            return self.conversations_inventory_client.get_conversations()

        @app.get("/v1/conversations/{conversationId}", tags = tags,
                 response_description = "Get a single conversation",
                 response_model = Conversation,
                 response_model_by_alias = False,)
        def get_conversation(conversationId: str):
            conversation = self.conversations_inventory_client.get_conversation(conversationId)
            if conversation is not None:
                return conversation
            raise HTTPException(status_code=404, detail=f"Unable to find conversation with {id}")
        
        @app.delete("/v1/conversations/{conversationId}", tags = tags, response_description = "Deletes a conversation")
        async def delete_conversation(conversationId: str):
            delete_result = self.conversations_inventory_client.delete_conversation(conversationId)
            if delete_result.deleted_count == 1:
                return Response(status_code = status.HTTP_204_NO_CONTENT)
            raise HTTPException(status_code=500, detail=f"Unable to delete conversation with {conversationId}")