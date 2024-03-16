from chat.models.conversation import Conversation, Message
from bson.objectid import ObjectId
from pymongo import MongoClient
import os


class ConversationCollection:
    def __init__(self):
        self.collection = MongoClient(os.environ["MONGO_DB_URL"])["talk-to-text"]["conversation"]

    def create_conversation(self, conversation: Conversation):
        result = self.collection.insert_one(conversation.model_dump(by_alias = True, exclude = ["id"]))
        new_conversation = self.collection.find_one({"_id": result.inserted_id})
        return new_conversation

    def add_message_to_conversation(self, message: Message, id: str):
        message_dict = message.model_dump(by_alias = True)
        result = self.collection.update_one(
            {"_id": ObjectId(id)},
            {"$push": {"messages": message_dict}}
        )
        if result.modified_count == 1:
           return True
        else:
            return False

    def get_conversations(self):
        conversations = list(self.collection.find())
        for conversation in conversations:
            conversation["_id"] = str(conversation["_id"])
        return conversations
    
    def get_conversation(self, id: str):
        conversation = self.collection.find_one({"_id": ObjectId(id)})
        if conversation:
            conversation["_id"] = str(conversation["_id"])
            return conversation
        else:
            return None
        
    def delete_conversation(self, id: str):
        conversation = self.collection.delete_one({"_id":  ObjectId(id)})
        return conversation