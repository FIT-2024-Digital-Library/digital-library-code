from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

from app.templates_processor import templates
from app.routes import books
from app.routes import users

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(books.router)
app.include_router(users.router)

@app.get("/", response_class=HTMLResponse)
async def main_page(request: Request):
    return templates.TemplateResponse(
        request=request, name="pages/main-page.html", context={"books": ["a", "b", "c"]}
    )
