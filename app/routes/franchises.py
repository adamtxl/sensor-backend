from fastapi import APIRouter, HTTPException
from app.models import Franchise
from app.crud.franchises import (
    add_franchise,
    get_franchises,
    update_franchise,
    soft_delete_franchise,
)
from fastapi import Depends
from app.auth import verify_token

router = APIRouter(dependencies=[Depends(verify_token)])

@router.post("/franchises")
async def create_franchise(franchise: Franchise):
    await add_franchise(franchise)
    return {"status": "franchise created"}

@router.get("/franchises")
async def list_franchises():
    return await get_franchises()

@router.get("/admin/franchises")
async def list_all_franchises_admin():
    return await get_franchises(include_deleted=True)

@router.put("/franchises/{franchise_id}")
async def update_franchise_info(franchise_id: int, franchise: Franchise):
    await update_franchise(franchise_id, franchise.name)
    return {"status": "franchise updated"}

@router.delete("/franchises/{franchise_id}")
async def delete_franchise(franchise_id: int):
    result = await soft_delete_franchise(franchise_id)
    if result == "UPDATE 0":
        raise HTTPException(status_code=404, detail="Franchise not found")
    return {"status": "franchise soft-deleted"}
