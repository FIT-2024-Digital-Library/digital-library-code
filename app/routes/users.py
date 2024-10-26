from fastapi import FastAPI, Request, APIRouter
from fastapi.responses import HTMLResponse, RedirectResponse

from app.templates_processor import templates

router = APIRouter(
    prefix='/users',
    tags=['user']
)

@router.get('/profile', response_class=HTMLResponse, summary='Returns user page')
async def get_profile(request: Request):
    raise NotImplemented
    # Здесь будет куча логики по поиску
    return templates.TemplateResponse(
        request=request, name='basic.html'
    )

@router.post('/login', response_class=RedirectResponse, summary='Logs user in')
async def login(request: Request):
    raise NotImplemented
    return RedirectResponse('/')

@router.post('/register', response_class=RedirectResponse, summary='Creates new user')
async def register(request: Request):
    raise NotImplemented
    return RedirectResponse('/')