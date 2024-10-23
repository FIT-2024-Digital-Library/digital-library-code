from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")


templates = Jinja2Templates(directory="templates")


@app.get("/books/{id}", response_class=HTMLResponse)
async def read_book(request: Request, id: str):
    return templates.TemplateResponse(
        request=request, name="book.html", context={"id": id}
    )
