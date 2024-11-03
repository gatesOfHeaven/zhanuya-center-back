from pydantic import BaseModel

from .entity import Building


class BuildingAsForeign(BaseModel):
    id: int
    address: str

    @staticmethod
    def to_json(building: Building):
        return BuildingAsForeign(
            id = building.id,
            address = building.address
        ).model_dump()