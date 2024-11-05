from fastapi import APIRouter

from app.templates_processor import templates

router = APIRouter(
    prefix='/books',
    tags=['book']
)

@router.get('/', response_model=None, summary='Returns books using search paraters (all of them otherwise)')
async def get_books():
    raise NotImplemented
    return {} # Here will be pydantic scheme's object

@router.get('/{id}', response_model=None, summary='Returns book data')
async def get_book(id: int):
    raise NotImplemented
    return {} # Here will be pydantic scheme's object

@router.post('/create', response_model=None, summary='Creates new book. Only for authorized user with admin previlegy')
async def create_book():
    raise NotImplemented
    return {} # Here will be pydantic scheme's object

@router.put('/{id}/update', response_model=None, summary='Updates book data. Only for authorized user with admin previlegy')
async def update_book(id: int):
    raise NotImplemented
    return {} # Here will be pydantic scheme's object

@router.delete('/{id}/delete', response_model=None, summary='Deletes book. Only for authorized user with admin previlegy')
async def delete_book(id: int):
    raise NotImplemented
    return {} # Here will be OK empty response