from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from db.base import get_db
from Service import LocationService
from schemas.location import LocationCreate, LocationUpdate, LocationResponse

router = APIRouter(prefix="/locations", tags=["locations"])

@router.post("/", response_model=LocationResponse, status_code=status.HTTP_201_CREATED)
async def create_location(location_data: LocationCreate, db: AsyncSession = Depends(get_db)):
    """Створення нової локації"""
    location_service = LocationService(db)
    try:
        location = await location_service.create_location(location_data)
        return location
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        ) from e

@router.get("/{location_id}", response_model=LocationResponse)
async def get_location_by_id(location_id: int, db: AsyncSession = Depends(get_db)):
    """Отримання локації за ID"""
    location_service = LocationService(db)
    location = await location_service.get_location_by_id(location_id)
    if not location:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Location with id {location_id} not found"
        )
    return location

@router.get("/", response_model=List[LocationResponse])
async def get_all_locations(db: AsyncSession = Depends(get_db)):
    """Отримання всіх локацій"""
    location_service = LocationService(db)
    locations = await location_service.get_all_locations()
    return locations

@router.put("/{location_id}", response_model=LocationResponse)
async def update_location(location_id: int, location_data: LocationUpdate, db: AsyncSession = Depends(get_db)):
    """Оновлення локації"""
    location_service = LocationService(db)
    try:
        location = await location_service.update_location(location_id, location_data)
        if not location:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Location with id {location_id} not found"
            )
        return location
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        ) from e

@router.delete("/{location_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_location(location_id: int, db: AsyncSession = Depends(get_db)):
    """Видалення локації"""
    location_service = LocationService(db)
    try:
        deleted = await location_service.delete_location(location_id)
        if not deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Location with id {location_id} not found"
            )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        ) from e
