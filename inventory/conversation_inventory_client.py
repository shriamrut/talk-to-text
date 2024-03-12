from uuid import UUID
from chat.models.conversation import CreateConversation, PostMessage
from text.models.text import CreateText

class ConversationInventoryClient:
    def __init__(self):
        pass
    def add_conversation(self, createConversation: CreateConversation):
        pass
    def post_message_to_conversation(self, postMessage: PostMessage, conversationId: UUID):
        pass
    def get_conversations(self):
        pass
    def get_conversation(self, conversationId: UUID):
        pass