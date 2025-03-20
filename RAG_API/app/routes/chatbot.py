from fastapi import APIRouter, HTTPException
from app.schemas.chatbot import ChatbotRequest, ChatbotResponse,Source

from langchain_openai import OpenAI, OpenAIEmbeddings
from langchain.prompts import PromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
from langchain_chroma import Chroma

from app.services.chatbot_llm import ChatbotService

chatbot_service = ChatbotService()



router = APIRouter(prefix="/api", tags=["Chatbot"])

@router.post("/chat", response_model=ChatbotResponse)
async def chat_with_bot(request: ChatbotRequest):
    """
    Chatbot API: Retrieves relevant context from ChromaDB and generates an AI response.
    """
    try:
        structured_answer, sources = chatbot_service.generate_chat_response(request.message,request.chat_history)

        return ChatbotResponse(message=structured_answer, sources=sources)

    except HTTPException as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")