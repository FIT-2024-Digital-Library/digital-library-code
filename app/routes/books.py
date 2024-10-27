from fastapi import Request, APIRouter
from fastapi.responses import HTMLResponse, RedirectResponse

from app.templates_processor import templates

router = APIRouter(
    prefix='/books',
    tags=['book']
)

@router.get('/', response_class=HTMLResponse)
async def get_books(request: Request):
    raise NotImplemented
    # Здесь будет куча логики по поиску
    return templates.TemplateResponse(
    request=request, name='basic.html'
    )

@router.get('/{id}', response_class=HTMLResponse)
async def get_book(request: Request, id: int):
    raise NotImplemented
    return templates.TemplateResponse(
    request=request, name='basic.html'
    )

@router.post('/create')
async def create_book(request: Request):
    raise NotImplemented
    return RedirectResponse('/')

@router.put('/{id}/update')
async def update_book(request: Request, id: int):
    raise NotImplemented
    return RedirectResponse('/')

@router.delete('/{id}/delete')
async def delete_book(request: Request, id: int):
    raise NotImplemented
    return RedirectResponse('/')