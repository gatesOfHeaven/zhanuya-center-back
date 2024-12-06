from core.bases import BaseResponse
from .entity import Price


class PriceAsPrimary(BaseResponse):
    typeId: int
    typeName: str
    price: int

    @staticmethod
    def to_json(price: Price):
        return PriceAsPrimary(
            typeId = price.type_id,
            typeName = price.appointment_type.name,
            price = price.cost
        ).model_dump()