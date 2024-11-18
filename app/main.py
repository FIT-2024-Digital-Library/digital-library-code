from fastapi import FastAPI

from app.routes import books, users, authors, genres

app = FastAPI()

app.include_router(books.router)
app.include_router(users.router)
app.include_router(authors.router)
app.include_router(genres.router)

