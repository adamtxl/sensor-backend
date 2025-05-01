from fastapi import APIRouter
from typing import List
from app.models import SensorReading
from app.crud.readings import insert_sensor_reading, get_sensor_readings, get_enriched_readings

router = APIRouter()

@router.post("/data")
async def create_reading(reading: SensorReading):
    await insert_sensor_reading(reading)
    return {"status": "ok"}

@router.get("/data", response_model=List[SensorReading])
async def read_readings(sensor_id: str = None):
    return await get_sensor_readings(sensor_id)


@router.get("/enriched", tags=["readings"])
async def read_enriched():
    return await get_enriched_readings()