from fastapi import FastAPI
from app.routes import upload, chatbot

app = FastAPI(title="RAG Chatbot API", version="1.0")

# Include Routes
app.include_router(upload.router)
app.include_router(chatbot.router)

