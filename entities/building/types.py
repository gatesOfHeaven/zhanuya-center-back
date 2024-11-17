from utils.bases import BaseResponse
from .entity import Building


class BuildingAsForeign(BaseResponse):
    id: int
    address: str

    @staticmethod
    def to_json(building: Building):
        return BuildingAsForeign(
            id = building.id,
            address = building.address
        ).model_dump()