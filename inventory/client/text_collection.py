from text.models.text import Text
from pymongo import MongoClient
import os

class TextCollection:
    def __init__(self):
        self.collection = MongoClient(os.environ["MONGO_DB_URL"])["talk-to-text"]["text"]

    def create(self, content: str, title: str):
        text = Text(content = content,
                    title = title)
        result = self.collection.insert_one(text.model_dump(by_alias=True, exclude = ["id"]))
        return result.inserted_id
    
    #TODO get, delete, and patch if needed