from pydantic import BaseModel


class BaseResponse(BaseModel):
    detail: str

    @staticmethod
    def to_json(detail: str):
        return BaseResponse(detail = detail).model_dump()