from uuid import UUID
from chat.models.conversation import Conversation, Message
from text.models.text import CreateText
from bson.objectid import ObjectId
from pymongo import MongoClient
import os
from fastapi import FastAPI, HTTPException, Body

class ConversationInventoryClient:
    def __init__(self):
        self.conversation_collection = MongoClient(os.environ["MONGO_DB_URL"])["talk-to-text"]["conversation"]

    def create_conversation(self, conversation: Conversation):
        #conversation_dict = conversation.dict()
        result = self.conversation_collection.insert_one(conversation.model_dump(by_alias = True, exclude = ["id"]))
        new_conversation = self.conversation_collection.find_one({"_id": result.inserted_id})
        return new_conversation

    def post_message_to_conversation(self, message: Message, id: str):
        message_dict = message.dict()
        result = self.conversation_collection.update_one(
            {"_id": ObjectId(id)},
            {"$push": {"messages": message_dict}}
        )
        if result.modified_count == 1:
           return True
        else:
            return False

    def get_conversations(self):
        conversations = list(self.conversation_collection.find())
        for conversation in conversations:
            conversation["_id"] = str(conversation["_id"])
        return conversations
    
    def get_conversation(self, id: str):
        conversation = self.conversation_collection.find_one({"_id": ObjectId(id)})
        if conversation:
            conversation["_id"] = str(conversation["_id"])
            return conversation
        else:
            return None
        
    def delete_conversation(self, id: str):
        conversation = self.conversation_collection.delete_one({"_id":  ObjectId(id)})
        return conversation