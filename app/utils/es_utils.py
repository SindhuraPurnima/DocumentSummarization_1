from elasticsearch import Elasticsearch
from fastapi import HTTPException

es = Elasticsearch(
    hosts=["https://localhost:9200"],
    basic_auth=("elastic", "PIyTHiodiOyFy7*Ey7MG"),
    verify_certs=False
)

def index_document(doc: dict):
    """
    Index the document in Elasticsearch.
    """
    try:
        response = es.index(index="documents", body=doc)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
def fetch_document_from_elasticsearch(doc_id: str):
    """
    Fetches a document from Elasticsearch using its ID.
    """
    try:
        response = es.get(index="documents", id=doc_id)
        if response["found"]:
            return response["_source"]  # Document content
        else:
            print(f"Document with ID {doc_id} not found in Elasticsearch.")
            return None
    except Exception as e:
        print(f"Error fetching document from Elasticsearch: {str(e)}")
        return None

