import os
from bson import ObjectId
from langchain.text_splitter import RecursiveCharacterTextSplitter
import chromadb

class EmbeddingCollection:
    def __init__(self, chunk_size = 50, chunk_overlap = 10, add_start_index=True):
        self.client = chromadb.HttpClient(host = os.environ['CHROMA_DB_URL'], 
                                          port = os.environ['CHROMA_DB_PORT'])

    def create(self, content, text_id, chunk_size, chunk_overlap):
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, 
                                                       chunk_overlap=chunk_overlap, 
                                                       add_start_index=True)
        collection = self.client.get_or_create_collection(name = "embeddings")
        splits = text_splitter.split_text(content)
        split_ids = [str(ObjectId()) for _ in range(len(splits))]
        metadatas = [{"text_id": str(text_id)} for _ in range(len(splits))]
        collection.add(documents=splits, 
                       metadatas=metadatas, 
                       ids = split_ids)

    def query(self, text_id, query_text):
        collection = self.client.get_or_create_collection(name = "embeddings")
        return collection.query(query_texts=[query_text],
                                n_results=10,
                                where={"text_id":text_id})