from typing import List
import uuid
from datetime import datetime
from uuid import UUID
from chat.models.conversation import Conversation, Message, CreateConversation, PostMessage
import logging

conversation_lists = []

class ConversationController:

    def __init__(self, app, tags):
        @app.post("/v1/conversations/", tags = tags)
        async def create_conversation(createConversation: CreateConversation) -> Conversation:
            textId = createConversation.textId
            logging.debug(f"Creating conversation on text with id {textId}")
            conversation = Conversation(messages = [], 
                                        textId = textId)
            conversation_lists.append(conversation)
            return conversation
        
        @app.post("/v1/conversations/{conversationId}/messages", tags = tags)
        async def post_message(conversationId: UUID, postMessage: PostMessage) -> Message:
            messageContent = postMessage.messageContent
            logging.debug(f"Got message from user: {messageContent}")
            selected_conversation = get_conversation(conversationId)
            message = Message(messageContent = messageContent,
                            isUser = True)
            selected_conversation.messages.append(message)
            response_message = Message(messageContent = "Hi, in WIP!",
                                       isUser = False)
            selected_conversation.messages.append(response_message)
            return response_message

        @app.get("/v1/conversations", tags = tags)
        def get_conversations() -> List[Conversation]:
            return conversation_lists

        @app.get("/v1/conversations/{conversationId}", tags = tags)
        def get_conversation(conversationId: UUID) -> Conversation:
            for conversation in conversation_lists:
                if conversation.conversationId == conversationId:
                    return conversation
            return {}