from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes import books, users, authors, genres, storage, reviews
from app.utils import create_tables, close_connections


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_tables()
    yield
    await close_connections()


app = FastAPI(lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:5173'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)

app.include_router(books.router)
app.include_router(users.router)
app.include_router(authors.router)
app.include_router(genres.router)
app.include_router(storage.router)
app.include_router(reviews.router)
####################################################################
####################################################################
####################################################################

from elasticsearch import Elasticsearch
from fastapi import BackgroundTasks, UploadFile, File
#from sentence_transformers import SentenceTransformer
import pdfplumber
import io

ELASTIC_API_PORT = 9200


"""
# Загрузка модели
__model = SentenceTransformer('all-MiniLM-L6-v2')  # Модель с размером вектора 384

def encode_text_to_vector(text: str):
    return __model.encode(text).tolist()  # Преобразуем в список для сохранения
"""

# Подключение к Elasticsearch
es = Elasticsearch(f"http://localhost:{ELASTIC_API_PORT}")

index_settings = {
    "settings": {
        "analysis": {
            "analyzer": {
                "default": {
                    "type": "standard"
                }
            }
        }
    },
    "mappings": {
        "dynamic": "strict",
        "properties": {
            "title": {"type": "text"},
            "author": {"type": "text"},
            "genre": {"type": "keyword"},
            "content": {"type": "text"}
        }
    }
}

def extract_pdf_text(content: bytes) -> str:
    # Используем io.BytesIO для создания файлового объекта из содержимого
    with pdfplumber.open(io.BytesIO(content)) as pdf:
        full_text = ""
        for page in pdf.pages:
            full_text += page.extract_text() + "\n"
    print("BOOK-PROCESSING: Finish extracting")
    return full_text

def index_book(book_id: str, title: str, author: str, genre: str, content: bytes):
    if not es.indices.exists(index="books"):
        es.indices.create(index="books", body=index_settings)
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
        es.index(index="books", id=book_id, body=document)
        print("BOOK-PROCESSING: Finish indexing")
    except Exception as e:
        print(f"Ошибка индексации: {e}")


@app.post("/upload-pdf")
async def upload_file(background_tasks: BackgroundTasks, file: UploadFile = File(...)):
    # Читаем содержимое файла
    content = await file.read()
    background_tasks.add_task(
        index_book,
        book_id="1",
        title="Системные требования",
        author="К.В. Козлов",
        genre="страх и ненависть",
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
    return es.search(index="books", body=search_body)


@app.get("/find-book")
def find_books(query: str):
    results = search_books(query)
    for hit in results['hits']['hits']:
        print(hit["_source"]["title"])
