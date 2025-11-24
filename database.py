import asyncpg
from config import DB_CONF

async def get_connection():
    return await asyncpg.connect(**DB_CONF)