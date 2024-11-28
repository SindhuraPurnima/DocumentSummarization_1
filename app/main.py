from fastapi import FastAPI
from .services.document_service import upload_document
from .services.health_check_service import health_check

app = FastAPI()

# Routes
@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI with Elasticsearch!"}

app.include_router(upload_document.router, prefix="/upload", tags=["upload"])
app.include_router(health_check.router, prefix="/health", tags=["health"])

