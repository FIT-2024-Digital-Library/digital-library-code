from fastapi import APIRouter

from app.crud.indexing import context_search_books
from app.settings import elastic_cred

router = APIRouter(
    prefix='/complex_search',
    tags=['complex_search']
)


@router.get("/context")#, response_model=list[int])
async def context_search(query: str):# -> list[int]:
    results: dict = await context_search_books(query)
    return [{"id":book["_id"], "score":book["_score"], "genre":book["_source"]["genre"]}
            for book in results['hits']['hits'] if book["_score"] >= elastic_cred.min_score]
