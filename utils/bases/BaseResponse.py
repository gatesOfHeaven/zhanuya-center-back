from pydantic import BaseModel


class BaseResponse(BaseModel):
    detail: str

    def to_json(detail: str):
        return BaseResponse(detail = detail).model_dump()