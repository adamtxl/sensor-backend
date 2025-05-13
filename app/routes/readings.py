from fastapi import APIRouter, Header, HTTPException
from typing import List, Optional
from app.models import SensorReading
from app.crud.readings import insert_sensor_reading, get_sensor_readings, get_enriched_readings
import os
from fastapi import Depends
from app.auth import verify_token


router = APIRouter(dependencies=[Depends(verify_token)])

API_KEY = os.getenv("READINGS_API_KEY", "supersecrettoken")

@router.post("/data")
async def create_reading(reading: SensorReading, authorization: str = Header(None)):
    if authorization != f"Bearer {API_KEY}":
        raise HTTPException(status_code=401, detail="Unauthorized")
    await insert_sensor_reading(reading)
    return {"status": "reading recorded"}

@router.get("/data", response_model=List[SensorReading])
async def read_readings(sensor_id: Optional[str] = None):
    return await get_sensor_readings(sensor_id)

@router.get("/enriched", tags=["readings"])
async def read_enriched():
    return await get_enriched_readings()
