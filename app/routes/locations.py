from fastapi import APIRouter
from app.crud import get_locations
from app.crud import get_sensors_by_location
router = APIRouter()

@router.get("/locations")
async def list_locations():
    return await get_locations()

@router.get("/locations/{location_id}/sensors")
async def list_sensors_at_location(location_id: int):
    return await get_sensors_by_location(location_id)