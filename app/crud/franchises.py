from app.db import connect
from app.models import Franchise

async def add_franchise(franchise: Franchise):
    conn = await connect()
    await conn.execute("""
        INSERT INTO franchises (name)
        VALUES ($1)
    """, franchise.name)
    await conn.close()

async def get_franchises(include_deleted: bool = False):
    conn = await connect()
    query = """
        SELECT id, name, created_on
        FROM franchises
    """
    if not include_deleted:
        query += " WHERE is_deleted = FALSE"
    rows = await conn.fetch(query)
    await conn.close()
    return [dict(r) for r in rows]

async def update_franchise(franchise_id: int, name: str):
    conn = await connect()
    result = await conn.execute("""
        UPDATE franchises
        SET name = $1
        WHERE id = $2
    """, name, franchise_id)
    await conn.close()
    return result


async def soft_delete_franchise(franchise_id: int):
    conn = await connect()
    result = await conn.execute("""
        UPDATE franchises
        SET is_deleted = TRUE
        WHERE id = $1
    """, franchise_id)
    await conn.close()
    return result
