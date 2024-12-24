import io, pdfplumber
from fastapi import HTTPException

from app.crud.books import BooksCrud
from app.crud.storage import Storage
from app.observer_pattern.observable_event import ObservableEvent
from app.observer_pattern.subscriber_interface import SubscriberInterface
from app.settings.elastic import elastic_cred, _es

"""
from sentence_transformers import SentenceTransformer

# Загрузка модели
__model = SentenceTransformer('all-MiniLM-L6-v2')  # Модель с размером вектора 384

def encode_text_to_vector(text: str):
    return __model.encode(text).tolist()  # Преобразуем в список для сохранения
"""


class Indexing:
    @classmethod
    def __extract_pdf_text(cls, content: bytes) -> str:
        # Используем io.BytesIO для создания файлового объекта из содержимого
        with pdfplumber.open(io.BytesIO(content)) as pdf:
            full_text = ""
            for page in pdf.pages:
                full_text += page.extract_text() + "\n"
        print("BOOK-PROCESSING: Finish extracting")
        return full_text

    @classmethod
    async def index_book(cls, book_id: int, genre: str, book_file_path: str):
        # Генерация вектора
        # content_vector = encode_text_to_vector(content)
        # Формирование документа
        book_text: str = cls.__extract_pdf_text(await Storage.download_file_bytes(book_file_path))
        document = {"genre": genre if genre is not None else "", "content": book_text}
        try:
            await _es.index(index=elastic_cred.books_index, id=str(book_id), body=document)
            print("BOOK-PROCESSING: Finish indexing")
        except Exception as e:
            raise HTTPException(status_code=418, detail=f"Indexation error: {e}")

    @classmethod
    async def delete_book(cls, book_id: int):
        try:
            await _es.delete(index=elastic_cred.books_index, id=str(book_id))
            print(f"BOOK-PROCESSING: Successfully deleted book with ID {book_id}")
        except Exception as e:
            raise HTTPException(status_code=418, detail=f"Deletion error: {e}")

    @classmethod
    async def context_search_books(cls, query):
        search_body = {
            "query": {
                "multi_match": {
                    "query": query,
                    "fields": ["genre", "content"]
                }
            }
        }
        return await _es.search(index=elastic_cred.books_index, body=search_body)

    """
    Как происходит поиск книги в этой функции:
    async def context_search_books(query):
        search_body = {
            "query": {
                "multi_match": {
                    "query": query,
                    "fields": ["genre", "content"]
                }
            }
        }
        return await _es.search(index=elastic_cred.books_index, body=search_body)
    """
