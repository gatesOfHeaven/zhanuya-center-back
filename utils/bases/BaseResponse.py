from pydantic import BaseModel
from typing import Generic, TypeVar


T = TypeVar('T')


class BaseResponse(BaseModel):
    detail: str

    @staticmethod
    def to_json(detail: str):
        return BaseResponse(detail = detail).model_dump()
    

class PaginationResponse(BaseModel, Generic[T]):
    start: int
    end: int
    total: int
    page: list[T]

    @staticmethod
    def to_json(offset: int, limit: int, total: int, page: list[T]):
        return PaginationResponse(
            start = offset,
            end = offset + limit,
            total = total,
            page = page
        ).model_dump()