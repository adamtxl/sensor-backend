from fastapi import APIRouter
from app.models import Franchise
from app.crud import add_franchise, get_franchises, update_franchise

router = APIRouter()

@router.post("/franchises")
async def create_franchise(franchise: Franchise):
    await add_franchise(franchise)
    return {"status": "franchise created"}

@router.get("/franchises")
async def list_franchises():
    return await get_franchises()

@router.put("/franchises/{franchise_id}")
async def update_franchise_info(franchise_id: int, franchise: Franchise):
    await update_franchise(franchise_id, franchise.name)
    return {"status": "franchise updated"}
