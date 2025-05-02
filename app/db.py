import asyncpg
import os
from dotenv import load_dotenv

load_dotenv() 

DATABASE_URL = os.getenv("DATABASE_URL")  

async def connect():
    return await asyncpg.connect(DATABASE_URL)

async def init_db():
    conn = await connect()
    await conn.execute("SELECT 1")  # sanity check
    await conn.close()
