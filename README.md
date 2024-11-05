# Digital Library

## Technology Stack and Features

- [**FastAPI**](https://fastapi.tiangolo.com) for the Python backend API.
- [Jinja](https://jinja.palletsprojects.com/en/3.1.x/) for dynamically generating HTML pages with embedded data and logic (server-side rendering).
- [Elasticsearch](https://www.elastic.co/elasticsearch) for semantic search.
- [SQLAlchemy](https://https://www.sqlalchemy.org/) for the Python SQL database interactions.
- [Pydantic](https://docs.pydantic.dev), used by FastAPI, for the data validation and settings management.
- [PostgreSQL 17](https://www.postgresql.org) as the SQL database.

## How to start the service
1. Execute next commands locating in project's root:
```bash
# To create a virtual environment, you can use the venv module that comes with Python
python -m venv .venv

# Activate the new virtual environment
# - On Windows PowerShell, run
.venv\Scripts\activate
# - On Unix or MacOs, run
source .venv/bin/activate
# Upgrade pip
python -m pip install --upgrade pip

# Install packages from requirements.txt
pip install -r requirements.txt
```
2. Install PostgreSQL and add its credentials as environment vars:
```conf
POSTGRES_HOSTNAME=localhost:5432
POSTGRES_DB_NAME=digital-library
POSTGRES_LOGIN=backend
POSTGRES_PASSWORD="t0p_s3cret!"
```
3. To create tables in DB, run:
```bash
python create_tables.py
```
4. Run service:
```bash
fastapi dev main.py
```

## Project description
...
