import asyncio
from app.database import create_tables

asyncio.run(create_tables())
