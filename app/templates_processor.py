from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="templates")

# TODO: по хорошему, генераторы темплейтов вынести тоже сюда из хэндеров либо писать их отдельными функциями рядом с хэндлерами