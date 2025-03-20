import os
from fastapi import HTTPException
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings


class VectorStoreService:
    def __init__(self):
        self.embeddings = OpenAIEmbeddings(api_key=os.environ.get("OPENAI_API_KEY"))

        # Service 5: Store chunks in vector database
    def store_in_vector_db(self, chunks):
        try:
            vector_store = Chroma.from_documents(persist_directory="./chroma_db", documents=chunks, embedding=self.embeddings)
            return vector_store
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error storing in vector database: {str(e)}")
        
    def create_vector_store(self):
        """Create and return a Chroma vector store."""
        try:
            vector_store = Chroma(persist_directory="./chroma_db", embedding_function=self.embeddings)
            return vector_store
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error initializing vector store: {str(e)}")

    def get_retriever(self, vector_store):
        """Create and return a retriever with similarity search."""
        return vector_store.as_retriever(search_type="similarity", search_kwargs={"k": 3})
