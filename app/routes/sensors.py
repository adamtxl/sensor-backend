from fastapi import APIRouter, HTTPException
from typing import Optional
from datetime import datetime
from app.models import Sensor
from app.crud import add_sensor, update_sensor, delete_sensor, get_sensors, soft_delete_sensor

router = APIRouter()

@router.post("/sensors")
async def create_sensor(sensor: Sensor):
    await add_sensor(sensor)
    return {"status": "sensor created"}

@router.put("/sensors/{sensor_id}")
async def modify_sensor(sensor_id: str, sensor: Sensor):
    result = await update_sensor(sensor_id, sensor)
    if result == "UPDATE 0":
        raise HTTPException(status_code=404, detail="Sensor not found")
    return {"status": "sensor updated"}

@router.delete("/sensors/{sensor_id}")
async def remove_sensor(sensor_id: str):
    result = await delete_sensor(sensor_id)
    if result == "DELETE 0":
        raise HTTPException(status_code=404, detail="Sensor not found")
    return {"status": "sensor deleted"}

@router.get("/sensors")
async def list_sensors(location_id: Optional[int] = None, installed_after: Optional[str] = None):
    return await get_sensors(location_id=location_id, installed_after=installed_after)

@router.get("/admin/sensors")
async def list_all_sensors_admin():
    return await get_sensors(include_deleted=True)

@router.delete("/sensors/{sensor_id}")
async def delete_sensor(sensor_id: str):
    result = await soft_delete_sensor(sensor_id)
    if result == "UPDATE 0":
        raise HTTPException(status_code=404, detail="Sensor not found")
    return {"status": "sensor soft-deleted"}
