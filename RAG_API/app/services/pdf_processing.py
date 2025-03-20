import os
import uuid
import hashlib
import fitz  # PyMuPDF
from fastapi import HTTPException
from langchain.text_splitter import RecursiveCharacterTextSplitter

from langchain.schema import Document

class PDFProcessor:

    # Service 1: Read the file and extract details
    async def read_file(self, file):
        try:
            filename = file.filename
            file_content = await file.read()
            file_extension = os.path.splitext(filename)[1].lower()
            return filename, file_content, file_extension
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error loading PDF: {str(e)}")

    # Service 2: Generate unique document ID
    def generate_document_id(self, filename):
        return str(uuid.UUID(bytes=hashlib.sha256(filename.encode()).digest()[:16]))

    # Service 3: Validate PDF and extract text content
    def extract_text_from_pdf(self, file_content):
        try:
            pdf_document = fitz.open(stream=file_content, filetype="pdf")
            content = "".join(page.get_text() for page in pdf_document)
            return content
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error processing PDF: {str(e)}")

    # Service 4: Split document into smaller chunks
    def split_document(self, content):
        try:
            document = Document(page_content=content, metadata={})
            text_splitter = RecursiveCharacterTextSplitter(chunk_size=2412, chunk_overlap=124)
            chunks = text_splitter.split_documents([document])
            return chunks
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error splitting document: {str(e)}")

   