import os
from bson import ObjectId
from langchain.text_splitter import RecursiveCharacterTextSplitter
import chromadb

class EmbeddingCollection:
    def __init__(self, chunk_size = 250, chunk_overlap = 200, add_start_index=True):
        self.client = chromadb.HttpClient(host = os.environ['CHROMA_DB_URL'], 
                                          port = os.environ['CHROMA_DB_PORT'])
        
        self.text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, 
                                                            chunk_overlap=chunk_overlap, 
                                                            add_start_index=add_start_index)
    def create(self, content, text_id):
        collection = self.client.get_or_create_collection(name = "embeddings")
        splits = self.text_splitter.split_text(content)
        split_ids = [str(ObjectId()) for _ in range(len(splits))]
        metadatas = [{"text_id": str(text_id)} for _ in range(len(splits))]
        collection.add(documents=splits, 
                       metadatas=metadatas, 
                       ids = split_ids)

    def query(self, query_text, text_id):
        collection = self.client.get_or_create_collection(name = "embeddings")
        return collection.query(query_texts=[query_text],
                                n_results=10,
                                where={"text_id":text_id})