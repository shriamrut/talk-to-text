from inventory.client.embedding_collection import EmbeddingCollection
from inventory.client.text_collection import TextCollection


class TextService:
    def __init__(self):
        self.text_collection = TextCollection()
        self.embedding_collection = EmbeddingCollection()

    def upload_text(self, content_in_bytes, title, chunk_size, chunk_overlap):
        file_content = content_in_bytes.decode("utf-8")
        id = self.text_collection.create(file_content, 
                                         title)
        self.embedding_collection.create(content=file_content, 
                                         text_id=id,
                                         chunk_size=chunk_size,
                                         chunk_overlap=chunk_overlap)
        return id
    
    def get_relevant_texts(self, text_id, query, reference_chunk_count):
        relevant_docs = self.embedding_collection.query(text_id = text_id, 
                                                   query_text = query,
                                                   reference_chunk_count = reference_chunk_count)
        return relevant_docs["documents"][0]