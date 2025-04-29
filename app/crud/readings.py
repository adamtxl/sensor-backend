from app.db import connect
from app.models import SensorReading
from datetime import datetime
from typing import Optional

async def insert_sensor_reading(reading: SensorReading):
    conn = await connect()
    await conn.execute("""
        INSERT INTO sensor_readings (sensor_id, type, value, timestamp)
        VALUES ($1, $2, $3, $4)
    """, reading.sensor_id, reading.type, reading.value, reading.timestamp or datetime.utcnow())
    await conn.close()

async def get_sensor_readings(sensor_id: Optional[str] = None):
    conn = await connect()
    if sensor_id:
        rows = await conn.fetch(
            "SELECT sensor_id, type, value, timestamp FROM sensor_readings WHERE sensor_id = $1",
            sensor_id
        )
    else:
        rows = await conn.fetch(
            "SELECT sensor_id, type, value, timestamp FROM sensor_readings"
        )
    await conn.close()
    return [dict(r) for r in rows]
