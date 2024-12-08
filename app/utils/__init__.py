from .crypt import *
from .database import *


class CrudException(BaseException):
    def __init__(self, *args):
        super().__init__(*args)
