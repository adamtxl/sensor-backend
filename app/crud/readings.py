from app.db import connect
from app.models import SensorReading
from datetime import datetime
from typing import Optional

async def insert_sensor_reading(reading: SensorReading):
    conn = await connect()
    await conn.execute("""
        INSERT INTO sensor_readings 
            (sensor_id, type, value, timestamp, rssi, snr, latitude, longitude, altitude)
        VALUES 
            ($1, $2, $3, $4, $5, $6, $7, $8, $9)
    """,
    reading.sensor_id,
    reading.type,
    reading.value,
    reading.timestamp or datetime.utcnow(),
    reading.rssi,
    reading.snr,
    reading.latitude,
    reading.longitude,
    reading.altitude)
    await conn.close()


async def get_sensor_readings(sensor_id: Optional[str] = None):
    conn = await connect()
    if sensor_id:
        rows = await conn.fetch("""
            SELECT sensor_id, type, value, timestamp, rssi, snr, latitude, longitude, altitude
            FROM sensor_readings
            WHERE sensor_id = $1
        """, sensor_id)
    else:
        rows = await conn.fetch("""
            SELECT sensor_id, type, value, timestamp, rssi, snr, latitude, longitude, altitude
            FROM sensor_readings
        """)
    await conn.close()
    return [dict(r) for r in rows]


async def get_enriched_readings():
    conn = await connect()
    rows = await conn.fetch("""
        SELECT 
            sr.sensor_id,
            sr.type,
            sr.value,
            sr.timestamp,
            sr.rssi,
            sr.snr,
            sr.latitude,
            sr.longitude,
            sr.altitude,
            l.name AS facility
        FROM sensor_readings sr
        JOIN sensors s ON sr.sensor_id = s.sensor_id
        JOIN locations l ON s.location_id = l.id
    """)
    await conn.close()
    return [dict(r) for r in rows]

