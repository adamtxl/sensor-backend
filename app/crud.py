from app.db import connect
from app.models import SensorReading, Sensor, Location, Franchise
from datetime import datetime
from typing import List, Optional
from app.models import Location

# Sensor Readings
async def insert_sensor_reading(reading: SensorReading):
    conn = await connect()
    await conn.execute("""
        INSERT INTO sensor_readings (sensor_id, type, value, timestamp)
        VALUES ($1, $2, $3, $4)
    """, reading.sensor_id, reading.type, reading.value, reading.timestamp or datetime.utcnow())
    await conn.close()

async def get_sensor_readings(sensor_id: str = None):
    conn = await connect()
    if sensor_id:
        rows = await conn.fetch("SELECT * FROM sensor_readings WHERE sensor_id=$1", sensor_id)
    else:
        rows = await conn.fetch("SELECT * FROM sensor_readings")
    await conn.close()
    return [dict(r) for r in rows]

# Sensor Metadata
async def add_sensor(sensor: Sensor):
    conn = await connect()
    await conn.execute("""
        INSERT INTO sensors (sensor_id, location_id, description, installed_on)
        VALUES ($1, $2, $3, $4)
    """, sensor.sensor_id, sensor.location_id, sensor.description, sensor.installed_on)
    await conn.close()


async def update_sensor(sensor_id: str, sensor: Sensor):
    conn = await connect()
    result = await conn.execute("""
        UPDATE sensors
        SET location = $1, description = $2, installed_on = $3
        WHERE sensor_id = $4
    """, sensor.location, sensor.description, sensor.installed_on, sensor_id)
    await conn.close()
    return result

async def delete_sensor(sensor_id: str):
    conn = await connect()
    result = await conn.execute("DELETE FROM sensors WHERE sensor_id = $1", sensor_id)
    await conn.close()
    return result


async def get_sensors(location_id: Optional[int] = None, installed_after: Optional[datetime] = None, include_deleted: bool = False):
    conn = await connect()

    base_query = """
        SELECT sensor_id, location_id, description, installed_on
        FROM sensors
    """
    filters = []
    values = []

    if not include_deleted:
        filters.append("is_deleted = FALSE")

    if location_id is not None:
        filters.append("location_id = $%d" % (len(values) + 1))
        values.append(location_id)

    if installed_after is not None:
        filters.append("installed_on >= $%d" % (len(values) + 1))
        values.append(installed_after)

    if filters:
        base_query += " WHERE " + " AND ".join(filters)

    rows = await conn.fetch(base_query, *values)
    await conn.close()
    return [dict(r) for r in rows]

async def update_sensor(sensor_id: str, sensor: Sensor):
    conn = await connect()
    result = await conn.execute("""
        UPDATE sensors
        SET location_id = $1, description = $2, installed_on = $3
        WHERE sensor_id = $4
    """, sensor.location_id, sensor.description, sensor.installed_on, sensor_id)
    await conn.close()
    return result

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


# Admin route to retrieve all items including deleted
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

async def soft_delete_sensor(sensor_id: str):
    conn = await connect()
    result = await conn.execute("""
        UPDATE sensors
        SET is_deleted = TRUE
        WHERE sensor_id = $1
    """, sensor_id)
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
