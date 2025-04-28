from fastapi import APIRouter
from app.models import Franchise
from app.crud import add_franchise, get_franchises

router = APIRouter()

@router.post("/franchises")
async def create_franchise(franchise: Franchise):
    await add_franchise(franchise)
    return {"status": "franchise created"}

@router.get("/franchises")
async def list_franchises():
    return await get_franchises()
