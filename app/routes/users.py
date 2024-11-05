from fastapi import APIRouter

router = APIRouter(
    prefix='/users',
    tags=['user']
)

@router.get('/profile', response_model=None, summary='Returns authorized user')
async def get_profile():
    raise NotImplemented
    return {} # Here will be pydantic scheme's object


@router.post('/login', response_model=None, summary='Logs user in')
async def login():
    raise NotImplemented
    return {} # Here will be pydantic scheme's object


@router.post('/register', response_model=None, summary='Creates new user')
async def register():
    raise NotImplemented
    return {} # Here will be pydantic scheme's object