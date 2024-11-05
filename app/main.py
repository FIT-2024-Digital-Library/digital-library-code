from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.routes import books
from app.routes import users


app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(books.router)
app.include_router(users.router)
