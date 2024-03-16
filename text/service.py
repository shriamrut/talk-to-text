from inventory.client.embedding_collection import EmbeddingCollection
from inventory.client.text_collection import TextCollection


class TextService:
    def __init__(self):
        self.text_collection = TextCollection()
        self.embedding_collection = EmbeddingCollection()

    def upload_text(self, content_in_bytes, title):
        file_content = content_in_bytes.decode("utf-8")
        id = self.text_collection.create(file_content, 
                                         title)
        self.embedding_collection.create(file_content, text_id=id)
        return id
    
    def get_relevant_texts(self, text_id, query):
        relevant_docs = self.embedding_collection.query(text_id = text_id, 
                                                   query_text = query)
        return relevant_docs["documents"][0]