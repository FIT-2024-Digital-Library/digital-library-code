import io, pdfplumber
from fastapi import APIRouter, BackgroundTasks, UploadFile, File
#from sentence_transformers import SentenceTransformer

from app.settings.elastic import _es, elastic_cred


router = APIRouter(
    prefix='/search',
    tags=['search']
)


"""
# Загрузка модели
__model = SentenceTransformer('all-MiniLM-L6-v2')  # Модель с размером вектора 384

def encode_text_to_vector(text: str):
    return __model.encode(text).tolist()  # Преобразуем в список для сохранения
"""


def extract_pdf_text(content: bytes) -> str:
    # Используем io.BytesIO для создания файлового объекта из содержимого
    with pdfplumber.open(io.BytesIO(content)) as pdf:
        full_text = ""
        for page in pdf.pages:
            full_text += page.extract_text() + "\n"
    print("BOOK-PROCESSING: Finish extracting")
    return full_text


def index_book(book_id: str, title: str, author: str, genre: str, content: bytes):
    # Генерация вектора
    # content_vector = encode_text_to_vector(content)
    # Формирование документа
    book_text: str = extract_pdf_text(content)
    document = {
        "title": title,
        "author": author,
        "genre": genre,
        "content": book_text,
    }
    # Индексация с обработкой ошибок
    try:
        _es.index(index=elastic_cred.books_index, id=book_id, body=document)
        print("BOOK-PROCESSING: Finish indexing")
    except Exception as e:
        print(f"Ошибка индексации: {e}")


@router.post("/upload-pdf")
async def upload_file(book_id: str, title: str, author: str, genre: str,
                      background_tasks: BackgroundTasks, file: UploadFile = File(...)):
    # Читаем содержимое файла
    content = await file.read()
    background_tasks.add_task(
        index_book,
        book_id=book_id,
        title=title,
        author=author,
        genre=genre,
        content=content
    )
    return {"filename": file.filename}


def search_books(query):
    search_body = {
        "query": {
            "multi_match": {
                "query": query,
                "fields": ["title^3", "author^2", "genre", "content"]
            }
        }
    }
    return _es.search(index=elastic_cred.books_index, body=search_body)


@router.get("/find-book")
def find_books(query: str):
    results: dict = search_books(query)
    return results['hits']['hits']
