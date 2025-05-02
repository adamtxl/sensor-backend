from fastapi import APIRouter, HTTPException
from app.models import Location
from app.crud.locations import add_location, get_locations, get_sensors_by_location, update_location, soft_delete_location

router = APIRouter()

@router.post("/locations")
async def create_location(location: Location):
    await add_location(location)
    return {"status": "location created"}

@router.get("/locations")
async def list_locations():
    return await get_locations()

@router.get("/admin/locations")
async def list_all_locations_admin():
    return await get_locations(include_deleted=True)



@router.get("/locations/{location_id}/sensors")
async def list_sensors_at_location(location_id: int):
    return await get_sensors_by_location(location_id)

@router.put("/locations/{location_id}")
async def update_location_info(location_id: int, location: Location):
    await update_location(location_id, location)
    return {"status": "location updated"}

@router.delete("/locations/{location_id}")
async def delete_location(location_id: int):
    result = await soft_delete_location(location_id)
    if result == "UPDATE 0":
        raise HTTPException(status_code=404, detail="Location not found")
    return {"status": "location soft-deleted"}
