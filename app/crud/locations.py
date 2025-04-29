from app.db import connect
from app.models import Location

async def add_location(location: Location):
    conn = await connect()
    await conn.execute("""
        INSERT INTO locations (name, address, city, state, zip, franchise_id)
        VALUES ($1, $2, $3, $4, $5, $6)
    """, location.name, location.address, location.city, location.state, location.zip, location.franchise_id)
    await conn.close()

async def get_locations(include_deleted: bool = False):
    conn = await connect()
    query = """
        SELECT id, name, address, city, state, zip, created_on
        FROM locations
    """
    if not include_deleted:
        query += " WHERE is_deleted = FALSE"
    rows = await conn.fetch(query)
    await conn.close()
    return [dict(r) for r in rows]

async def update_location(location_id: int, location: Location):
    conn = await connect()
    result = await conn.execute("""
        UPDATE locations
        SET name = $1, address = $2, city = $3, state = $4, zip = $5, franchise_id = $6
        WHERE id = $7
    """, location.name, location.address, location.city, location.state, location.zip, location.franchise_id, location_id)
    await conn.close()
    return result

async def soft_delete_location(location_id: int):
    conn = await connect()
    result = await conn.execute("""
        UPDATE locations
        SET is_deleted = TRUE
        WHERE id = $1
    """, location_id)
    await conn.close()
    return result

async def get_sensors_by_location(location_id: int):
    conn = await connect()
    rows = await conn.fetch("""
        SELECT sensor_id, type, value, timestamp
        FROM sensor_readings
        WHERE sensor_id IN (
            SELECT sensor_id
            FROM sensors
            WHERE location_id = $1
        )
    """, location_id)
    await conn.close()
    return [dict(r) for r in rows]
