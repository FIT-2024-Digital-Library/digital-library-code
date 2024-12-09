from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes import books, users, authors, genres, storage
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
####################################################################
####################################################################
####################################################################


from fastapi import UploadFile, File
import pdfplumber
import io


@app.post("/upload-pdf/")
async def upload_file(file: UploadFile = File(...)):
    # Читаем содержимое файла
    contents = await file.read()

    # Используем io.BytesIO для создания файлового объекта из содержимого
    with pdfplumber.open(io.BytesIO(contents)) as pdf:
        full_text = ""
        for page in pdf.pages:
            full_text += page.extract_text()

    return {"filename": file.filename, "content": full_text}
