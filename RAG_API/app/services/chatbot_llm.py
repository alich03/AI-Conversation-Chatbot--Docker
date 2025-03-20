
from langchain_openai import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
from fastapi import  HTTPException
from app.schemas.chatbot import Source
from app.services.vector_store import VectorStoreService
from langchain.chains import ConversationalRetrievalChain

import os


class ChatbotService:
    def __init__(self):
        self.llm = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
        self.vector_store_service = VectorStoreService()


    def generate_chat_response(self, request_message: str, chat_history):
        """Generate chatbot response by retrieving relevant context and generating an answer."""
        try:
            # 🔹 Define the chatbot prompt template
            retrieval_qa_chat_prompt = PromptTemplate(
                input_variables=["context", "question"],
                template="""
                    %INSTRUCTIONS:
                    You are a chatbot created by Ali Hasnain. Your role is to assist users with the provided data, offering clear, polite, and helpful responses. Additionally, you should provide general information when needed.

                    %CONTEXT: {context}

                    %QUESTION: {question}
                """
            )

            # 🔹 Create the retriever
            vector_store = self.vector_store_service.create_vector_store()
            retriever = self.vector_store_service.get_retriever(vector_store)

            # 🔹 Create a ConversationalRetrievalChain with a custom prompt
            crc = ConversationalRetrievalChain.from_llm(
                llm=self.llm,
                retriever=retriever,
                combine_docs_chain_kwargs={"prompt": retrieval_qa_chat_prompt}  # 👈 Inject custom prompt
            )

            # 🔹 Invoke the chain
            response = crc.invoke({
                'question': request_message,
                'chat_history': chat_history  # 🔹 Pass chat history
            })

            structured_answer = response.get("answer", "No response generated.")
            context = response.get("context", [])

            # 🔹 Extract sources from retrieved context
            sources = [
                {
                    "document_id": doc.metadata.get("document_id", "unknown"),
                    "filename": doc.metadata.get("filename", "unknown"),
                    "snippet": doc.page_content[:200]
                }
                for doc in context
            ]

            return structured_answer, sources

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error generating response: {str(e)}")
