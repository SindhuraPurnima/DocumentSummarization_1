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

def check_es_health() -> bool:
    """
    Check the health of the Elasticsearch cluster.
    """
    try:
        return es.ping()
    except Exception:
        return False
