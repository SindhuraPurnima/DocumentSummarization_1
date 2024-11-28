from fastapi import APIRouter, File, UploadFile, HTTPException
from ..utils.file_utils import extract_text_from_pdf, extract_text_from_word
from ..utils.es_utils import index_document
import io

router = APIRouter()

@router.post("/")
async def upload_document(file: UploadFile = File(...)):
    if not file:
        raise HTTPException(status_code=400, detail="No file received")
    file_content = await file.read()

    # Handle different file formats
    document_text = ""
    try:
        # Handle PDF files
        if file.content_type == "application/pdf":
            document_text = extract_text_from_pdf(file_content)

        # Handle Word files
        elif file.content_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            document_text = extract_text_from_word(file_content)

        # Handle text files (plain text)
        elif file.content_type == "text/plain":
            document_text = file_content.decode("utf-8")
        else:
            raise HTTPException(status_code=415, detail="Unsupported file type")

        # Index the document in Elasticsearch
        doc = {
            "content": document_text,
            "filename": file.filename,
            "content_type": file.content_type
        }

        # Store document in Elasticsearch
        response = index_document(doc)
        return {"message": "Document uploaded successfully!", "es_response": response}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
