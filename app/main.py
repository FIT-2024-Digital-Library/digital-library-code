from fastapi import FastAPI

from app.routes import books, users, authors, genres
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.include_router(books.router)
app.include_router(users.router)
app.include_router(authors.router)
app.include_router(genres.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:5173'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)
