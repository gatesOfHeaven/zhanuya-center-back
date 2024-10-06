from pydantic import BaseModel

from .entity import Office


class OfficeAsForeign(BaseModel):
    id: int
    city: str
    address: str
    room: str

    def to_json(office: Office):
        return OfficeAsForeign(
            id = office.id,
            city = office.city,
            address = office.address,
            room = office.room
        ).model_dump()