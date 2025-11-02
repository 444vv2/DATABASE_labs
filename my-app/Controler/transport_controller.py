from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from db.base import get_db
from Service import TransportService
from schemas.bus import BusCreate, BusUpdate, BusResponse
from schemas.plane import PlaneCreate, PlaneUpdate, PlaneResponse
from schemas.train import TrainCreate, TrainUpdate, TrainResponse

router = APIRouter(prefix="/transports", tags=["transports"])

@router.post("/buses/", response_model=BusResponse, status_code=status.HTTP_201_CREATED)
async def create_bus(bus_data: BusCreate, db: AsyncSession = Depends(get_db)):
    """Створення нового автобуса"""
    try:
        bus = await TransportService.create_bus(db, bus_data)
        return bus
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        ) from e

@router.get("/buses/{bus_id}", response_model=BusResponse)
async def get_bus_by_id(bus_id: int, db: AsyncSession = Depends(get_db)):
    """Отримання автобуса за ID"""
    bus = await TransportService.get_bus_by_id(db, bus_id)
    if not bus:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Bus with id {bus_id} not found"
        )
    return bus

@router.get("/buses/", response_model=List[BusResponse])
async def get_all_buses(db: AsyncSession = Depends(get_db)):
    """Отримання всіх автобусів"""
    buses = await TransportService.get_all_buses(db)
    return buses

@router.put("/buses/{bus_id}", response_model=BusResponse)
async def update_bus_by_id(bus_id: int, bus_data: BusUpdate, db: AsyncSession = Depends(get_db)):
    """Оновлення автобуса"""
    try:
        bus = await TransportService.update_bus(db, bus_id, bus_data)
        if not bus:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Bus with id {bus_id} not found"
            )
        return bus
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        ) from e

@router.delete("/buses/{bus_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_bus_by_id(bus_id: int, db: AsyncSession = Depends(get_db)):
    """Видалення автобуса"""
    try:
        deleted = await TransportService.delete_bus_by_id(db, bus_id)
        if not deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Bus with id {bus_id} not found"
            )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        ) from e

@router.post("/planes/", response_model=PlaneResponse, status_code=status.HTTP_201_CREATED)
async def create_plane(plane_data: PlaneCreate, db: AsyncSession = Depends(get_db)):
    """Створення нового літака"""
    try:
        plane = await TransportService.create_plane(db, plane_data)
        return plane
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        ) from e

@router.get("/planes/{plane_id}", response_model=PlaneResponse)
async def get_plane_by_id(plane_id: int, db: AsyncSession = Depends(get_db)):
    """Отримання літака за ID"""
    plane = await TransportService.get_plane_by_id(db, plane_id)
    if not plane:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Plane with id {plane_id} not found"
        )
    return plane

@router.get("/planes/", response_model=List[PlaneResponse])
async def get_all_planes(db: AsyncSession = Depends(get_db)):
    """Отримання всіх літаків"""
    planes = await TransportService.get_all_planes(db)
    return planes

@router.put("/planes/{plane_id}", response_model=PlaneResponse)
async def update_plane_by_id(plane_id: int, plane_data: PlaneUpdate, db: AsyncSession = Depends(get_db)):
    """Оновлення літака"""
    try:
        plane = await TransportService.update_plane(db, plane_id, plane_data)
        if not plane:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Plane with id {plane_id} not found"
            )
        return plane
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        ) from e

@router.delete("/planes/{plane_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_plane_by_id(plane_id: int, db: AsyncSession = Depends(get_db)):
    """Видалення літака"""
    try:
        deleted = await TransportService.delete_plane_by_id(db, plane_id)
        if not deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Plane with id {plane_id} not found"
            )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        ) from e

@router.post("/trains/", response_model=TrainResponse, status_code=status.HTTP_201_CREATED)
async def create_train(train_data: TrainCreate, db: AsyncSession = Depends(get_db)):
    """Створення нового поїзда"""
    try:
        train = await TransportService.create_train(db, train_data)
        return train
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        ) from e

@router.get("/trains/{train_id}", response_model=TrainResponse)
async def get_train_by_id(train_id: int, db: AsyncSession = Depends(get_db)):
    """Отримання поїзда за ID"""
    train = await TransportService.get_train_by_id(db, train_id)
    if not train:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Train with id {train_id} not found"
        )
    return train

@router.get("/trains/", response_model=List[TrainResponse])
async def get_all_trains(db: AsyncSession = Depends(get_db)):
    """Отримання всіх поїздів"""
    trains = await TransportService.get_all_trains(db)
    return trains

@router.put("/trains/{train_id}", response_model=TrainResponse)
async def update_train_by_id(train_id: int, train_data: TrainUpdate, db: AsyncSession = Depends(get_db)):
    """Оновлення поїзда"""
    try:
        train = await TransportService.update_train(db, train_id, train_data)
        if not train:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Train with id {train_id} not found"
            )
        return train
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        ) from e

@router.delete("/trains/{train_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_train_by_id(train_id: int, db: AsyncSession = Depends(get_db)):
    """Видалення поїзда"""
    try:
        deleted = await TransportService.delete_train_by_id(db, train_id)
        if not deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Train with id {train_id} not found"
            )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        ) from e
