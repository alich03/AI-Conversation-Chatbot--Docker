from fastapi import APIRouter, UploadFile, File, HTTPException
from app.schemas.upload import UploadResponse
from langchain.schema import Document
from dotenv import load_dotenv
load_dotenv()

from app.services.pdf_processing import PDFProcessor
from app.services.vector_store import VectorStoreService

router = APIRouter(prefix="/api", tags=["Document Upload"])

pdf_processor = PDFProcessor()
vector_db = VectorStoreService()

@router.post("/upload", response_model=UploadResponse)
async def upload_pdf(file: UploadFile = File(...)):
    """
    Upload a PDF document, extract its text, and store it in ChromaDB.
    """
    try:
        # Step 1: Read file details
        filename, file_content, file_extension = await pdf_processor.read_file(file)
        
        # Step 2: Validate file extension
        if file_extension != ".pdf":
            raise HTTPException(status_code=400, detail="Only PDF files are allowed.")

        # Step 3: Generate document ID
        document_id = pdf_processor.generate_document_id(filename)
        
        # Step 4: Extract text from PDF
        content = pdf_processor.extract_text_from_pdf(file_content)

        if not content:
            raise HTTPException(status_code=400, detail="File is empty.")
        if not content.strip():
            raise HTTPException(status_code=400, detail="Could not extract text from PDF.")


        
        # Step 5: Create document object
        document = Document(
            page_content=content,
            metadata={
                "source": filename,
                "document_id": document_id,
                "filename": filename,
                "file_extension": file_extension,
            },
        )

        # Step 6: Split the document into smaller chunks
        chunks = pdf_processor.split_document(content)

        # Step 7: Store chunks in vector database
        vector_db.store_in_vector_db(chunks)

        # Return the response with document_id
        return UploadResponse(message="PDF uploaded and processed successfully", document_id=document_id)

    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
