from fastapi import APIRouter

from app.crud.indexing import context_search_books, semantic_search_books
from app.settings import elastic_cred

router = APIRouter(
    prefix='/complex_search',
    tags=['complex_search']
)


@router.get("/context")#, response_model=list[int])
async def context_search(query: str):# -> list[int]:
    results: dict = await context_search_books(query)
    return [{"id":book["_id"], "score":book["_score"], "genre":book["_source"]["genre"]}
            for book in results['hits']['hits'] if book["_score"] >= elastic_cred.min_content_score]


@router.get("/semantic")
async def semantic_search(query: str):
    results: dict = await semantic_search_books(query)
    if results is None:
        return []
    return [{"id":book["_id"], "score":book["_score"], "genre":book["_source"]["genre"]}
            for book in results['hits']['hits'] if book["_score"] >= elastic_cred.min_semantic_score]
