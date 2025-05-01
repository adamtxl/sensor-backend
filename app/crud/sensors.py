from app.db import connect
from app.models import Sensor
from datetime import datetime
from typing import Optional

async def add_sensor(sensor: Sensor):
    conn = await connect()
    await conn.execute("""
        INSERT INTO sensors (sensor_id, location_id, description, installed_on, type)
        VALUES ($1, $2, $3, $4, $5)
    """, sensor.sensor_id, sensor.location_id, sensor.description, sensor.installed_on, sensor.type)
    await conn.close()

async def get_sensors(location_id: Optional[int] = None, installed_after: Optional[datetime] = None, include_deleted: bool = False):
    conn = await connect()

    base_query = """
        SELECT sensor_id, location_id, description, installed_on, type
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
        SET location_id = $1, description = $2, installed_on = $3, type = $4
        WHERE sensor_id = $5
    """, sensor.location_id, sensor.description, sensor.installed_on, sensor.type, sensor_id)
    await conn.close()
    return result

async def soft_delete_sensor(sensor_id: str):
    conn = await connect()
    result = await conn.execute("""
        UPDATE sensors
        SET is_deleted = TRUE
        WHERE sensor_id = $1
    """, sensor_id)
    await conn.close()
    return result
