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
    transport_service = TransportService(db)
    try:
        bus = await transport_service.create_bus(bus_data)
        return bus
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        ) from e

@router.get("/buses/{bus_id}", response_model=BusResponse)
async def get_bus_by_id(bus_id: int, db: AsyncSession = Depends(get_db)):
    """Отримання автобуса за ID"""
    transport_service = TransportService(db)
    bus = await transport_service.get_bus_by_id(bus_id)
    if not bus:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Bus with id {bus_id} not found"
        )
    return bus

@router.get("/buses/", response_model=List[BusResponse])
async def get_all_buses(db: AsyncSession = Depends(get_db)):
    """Отримання всіх автобусів"""
    transport_service = TransportService(db)
    buses = await transport_service.get_all_buses()
    return buses

@router.put("/buses/{bus_id}", response_model=BusResponse)
async def update_bus_by_id(bus_id: int, bus_data: BusUpdate, db: AsyncSession = Depends(get_db)):
    """Оновлення автобуса"""
    transport_service = TransportService(db)
    try:
        bus = await transport_service.update_bus(bus_id, bus_data)
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
    transport_service = TransportService(db)
    try:
        deleted = await transport_service.delete_bus(bus_id)
        if not deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Bus with id {bus_id} not found"
            )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        ) from e

@router.post("/planes/", response_model=PlaneResponse, status_code=status.HTTP_201_CREATED)
async def create_plane(plane_data: PlaneCreate, db: AsyncSession = Depends(get_db)):
    """Створення нового літака"""
    transport_service = TransportService(db)
    try:
        plane = await transport_service.create_plane(plane_data)
        return plane
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        ) from e

@router.get("/planes/{plane_id}", response_model=PlaneResponse)
async def get_plane_by_id(plane_id: int, db: AsyncSession = Depends(get_db)):
    """Отримання літака за ID"""
    transport_service = TransportService(db)
    plane = await transport_service.get_plane_by_id(plane_id)
    if not plane:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Plane with id {plane_id} not found"
        )
    return plane

@router.get("/planes/", response_model=List[PlaneResponse])
async def get_all_planes(db: AsyncSession = Depends(get_db)):
    """Отримання всіх літаків"""
    transport_service = TransportService(db)
    planes = await transport_service.get_all_planes()
    return planes

@router.put("/planes/{plane_id}", response_model=PlaneResponse)
async def update_plane_by_id(plane_id: int, plane_data: PlaneUpdate, db: AsyncSession = Depends(get_db)):
    """Оновлення літака"""
    transport_service = TransportService(db)
    try:
        plane = await transport_service.update_plane(plane_id, plane_data)
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
    transport_service = TransportService(db)
    try:
        deleted = await transport_service.delete_plane(plane_id)
        if not deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Plane with id {plane_id} not found"
            )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        ) from e

@router.post("/trains/", response_model=TrainResponse, status_code=status.HTTP_201_CREATED)
async def create_train(train_data: TrainCreate, db: AsyncSession = Depends(get_db)):
    """Створення нового поїзда"""
    transport_service = TransportService(db)
    try:
        train = await transport_service.create_train(train_data)
        return train
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        ) from e

@router.get("/trains/{train_id}", response_model=TrainResponse)
async def get_train_by_id(train_id: int, db: AsyncSession = Depends(get_db)):
    """Отримання поїзда за ID"""
    transport_service = TransportService(db)
    train = await transport_service.get_train_by_id(train_id)
    if not train:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Train with id {train_id} not found"
        )
    return train

@router.get("/trains/", response_model=List[TrainResponse])
async def get_all_trains(db: AsyncSession = Depends(get_db)):
    """Отримання всіх поїздів"""
    transport_service = TransportService(db)
    trains = await transport_service.get_all_trains()
    return trains

@router.put("/trains/{train_id}", response_model=TrainResponse)
async def update_train_by_id(train_id: int, train_data: TrainUpdate, db: AsyncSession = Depends(get_db)):
    """Оновлення поїзда"""
    transport_service = TransportService(db)
    try:
        train = await transport_service.update_train(train_id, train_data)
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
    transport_service = TransportService(db)
    try:
        deleted = await transport_service.delete_train(train_id)
        if not deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Train with id {train_id} not found"
            )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        ) from e
