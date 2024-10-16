from pydantic import BaseModel

from .entity import Price


class PriceAsPrimary(BaseModel):
    typeId: int
    typeName: str
    halfHourPrice: int

    def to_json(price: Price):
        return PriceAsPrimary(
            typeId = price.type_id,
            typeName = price.appointment_type.name,
            halfHourPrice = price.half_hour_price
        ).model_dump()