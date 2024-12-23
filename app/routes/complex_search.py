from fastapi import APIRouter

from app.crud.indexing import context_search_books
from app.settings import elastic_cred

router = APIRouter(
    prefix='/complex_search',
    tags=['complex_search']
)


"""
from sentence_transformers import SentenceTransformer

# Загрузка модели
__model = SentenceTransformer('all-MiniLM-L6-v2')  # Модель с размером вектора 384

def encode_text_to_vector(text: str):
    return __model.encode(text).tolist()  # Преобразуем в список для сохранения
"""


@router.get("/context")#, response_model=list[int])
async def context_search(query: str):# -> list[int]:
    results: dict = await context_search_books(query)
    return [book for book in results['hits']['hits'] if book["_score"] >= elastic_cred.min_score]
