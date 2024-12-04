from fastapi import FastAPI
from .services.document_service import uploadrouter

app = FastAPI()

# Routes
@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI with Elasticsearch!"}

app.include_router(uploadrouter, prefix="/upload", tags=["upload"])


