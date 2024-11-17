from utils.bases import BaseResponse
from .entity import Room


class RoomAsPrimary(BaseResponse):
    id: int
    building_id: int
    address: str
    title: str

    @staticmethod
    def to_json(room: Room):
        return RoomAsPrimary(
            id = room.id,
            building_id = room.building_id,
            address = room.building.address,
            title = room.title
        ).model_dump()