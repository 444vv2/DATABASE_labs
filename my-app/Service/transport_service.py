from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_

from DAO.general_dao import GeneralDAO
from db.models import Bus, Train, Plane
from schemas.bus import BusCreate, BusUpdate, BusResponse
from schemas.train import TrainCreate, TrainUpdate, TrainResponse
from schemas.plane import PlaneCreate, PlaneUpdate, PlaneResponse


class TransportService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.general_dao_bus = GeneralDAO[Bus](session)
        self.general_dao_train = GeneralDAO[Train](session)
        self.general_dao_plane = GeneralDAO[Plane](session)

    async def create_bus(self, bus_data: BusCreate) -> BusResponse:
        new_bus = Bus(
            departure_time=bus_data.departure_time,
            arrival_time=bus_data.arrival_time,
            from_id=bus_data.from_id,
            to_id=bus_data.to_id,
            seat_amount=bus_data.seat_amount
        )
        created_bus = await self.general_dao.create(new_bus)
        return BusResponse.model_validate(created_bus)

    async def create_train(self, train_data: TrainCreate) -> TrainResponse:
        new_train = Train(
            train_class=train_data.train_class,
            departure_time=train_data.departure_time,
            arrival_time=train_data.arrival_time,
            from_id=train_data.from_id,
            to_id=train_data.to_id,
            seat_amount=train_data.seat_amount
        )
        created_train = await self.general_dao.create(new_train)
        return TrainResponse.model_validate(created_train)

    async def create_plane(self, plane_data: PlaneCreate) -> PlaneResponse:
        new_plane = Plane(
                plane_class=plane_data.plane_class,
                departure_time=plane_data.departure_time,
                arrival_time=plane_data.arrival_time,
                from_id=plane_data.from_id,
                to_id=plane_data.to_id,
                seat_amount=plane_data.seat_amount
        )
        created_plane = await self.general_dao.create(new_plane)
        return PlaneResponse.model_validate(created_plane)

    async def get_bus_by_id(self, bus_id: int) -> Optional[BusResponse]:
        bus = await self.general_dao.get_by_id(Bus, bus_id)
        if bus:
            return BusResponse.model_validate(bus)
        return None

    async def get_train_by_id(self, train_id: int) -> Optional[TrainResponse]:
        train = await self.general_dao.get_by_id(Train, train_id)
        if train:
            return TrainResponse.model_validate(train)
        return None

    async def get_plane_by_id(self, plane_id: int) -> Optional[PlaneResponse]:
        plane = await self.general_dao.get_by_id(Plane, plane_id)
        if plane:
            return PlaneResponse.model_validate(plane)
        return None

    async def update_bus(self, bus_id: int, bus_data: BusUpdate) -> Optional[BusResponse]:
        bus = await self.general_dao.get_by_id(Bus, bus_id)
        if not bus:
            return None

        for field, value in bus_data.model_dump(exclude_unset=True).items():
            setattr(bus, field, value)

        updated_bus = await self.general_dao.update(bus)
        return BusResponse.model_validate(updated_bus)

    async def update_train(self, train_id: int, train_data: TrainUpdate) -> Optional[TrainResponse]:
        train = await self.general_dao.get_by_id(Train, train_id)
        if not train:
            return None

        for field, value in train_data.model_dump(exclude_unset=True).items():
            setattr(train, field, value)

        updated_train = await self.general_dao.update(train)
        return TrainResponse.model_validate(updated_train)

    async def update_plane(self, plane_id: int, plane_data: PlaneUpdate) -> Optional[PlaneResponse]:
        plane = await self.general_dao.get_by_id(Plane, plane_id)
        if not plane:
            return None

        for field, value in plane_data.model_dump(exclude_unset=True).items():
            setattr(plane, field, value)

        updated_plane = await self.general_dao.update(plane)
        return PlaneResponse.model_validate(updated_plane)

    async def delete_bus(self, bus_id: int) -> bool:
        result = await self.general_dao.delete_by_id(Bus, bus_id)
        return result

    async def delete_train(self, train_id: int) -> bool:
        result = await self.general_dao.delete_by_id(Train, train_id)
        return result

    async def delete_plane(self, plane_id: int) -> bool:
        result = await self.general_dao.delete_by_id(Plane, plane_id)
        return result

    async def get_all_buses(self) -> List[BusResponse]:
        buses = await self.general_dao.get_all(Bus)
        return [BusResponse.model_validate(bus) for bus in buses]

    async def get_all_trains(self) -> List[TrainResponse]:
        trains = await self.general_dao.get_all(Train)
        return [TrainResponse.model_validate(train) for train in trains]

    async def get_all_planes(self) -> List[PlaneResponse]:
        planes = await self.general_dao.get_all(Plane)
        return [PlaneResponse.model_validate(plane) for plane in planes]

    async def get_buses_by_route(self, from_id: int, to_id: int) -> List[BusResponse]:
        query = await self.session.execute(
            select(Bus).where(and_(Bus.from_id == from_id, Bus.to_id == to_id))
        )
        buses = query.scalars().all()
        return [BusResponse.model_validate(bus) for bus in buses]

    async def get_trains_by_route(self, from_id: int, to_id: int) -> List[TrainResponse]:
        query = await self.session.execute(
            select(Train).where(and_(Train.from_id == from_id, Train.to_id == to_id))
        )
        trains = query.scalars().all()
        return [TrainResponse.model_validate(train) for train in trains]

    async def get_planes_by_route(self, from_id: int, to_id: int) -> List[PlaneResponse]:
        query = await self.session.execute(
            select(Plane).where(and_(Plane.from_id == from_id, Plane.to_id == to_id))
        )
        planes = query.scalars().all()
        return [PlaneResponse.model_validate(plane) for plane in planes]
