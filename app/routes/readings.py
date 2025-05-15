from fastapi import APIRouter, Header, HTTPException
from typing import List, Optional
from app.models import SensorReading
from app.crud.readings import insert_sensor_reading, get_sensor_readings, get_enriched_readings
import os
import logging
from logging.handlers import RotatingFileHandler
from fastapi import Depends
from app.auth import verify_token


# Set up log formatting
log_formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

# Set up console handler
console_handler = logging.StreamHandler()
console_handler.setFormatter(log_formatter)
console_handler.setLevel(logging.INFO)

# Set up rotating file handler
file_handler = RotatingFileHandler(
    "backend_logs.log", 
    maxBytes=5*1024*1024,  # 5 MB
    backupCount=3          # Keep up to 3 old log files
)
file_handler.setFormatter(log_formatter)
file_handler.setLevel(logging.INFO)

# Set up the root logger
logging.basicConfig(
    level=logging.INFO,
    handlers=[console_handler, file_handler]
)



router = APIRouter(dependencies=[Depends(verify_token)])

API_KEY = os.getenv("READINGS_API_KEY", "supersecrettoken")

@router.post("/data")
async def create_reading(reading: SensorReading, authorization: str = Header(None)):
    if authorization != f"Bearer {API_KEY}":
        raise HTTPException(status_code=401, detail="Unauthorized")
    logging.info(f"Received reading: Sensor ID={reading.sensor_id}, Type={reading.type}, Value={reading.value}, Timestamp={reading.timestamp}, RSSI={reading.rssi}, SNR={reading.snr}")
    await insert_sensor_reading(reading)
    return {"status": "reading recorded"}

@router.get("/data", response_model=List[SensorReading])
async def read_readings(sensor_id: Optional[str] = None):
    return await get_sensor_readings(sensor_id)

@router.get("/enriched", tags=["readings"])
async def read_enriched():
    return await get_enriched_readings()
