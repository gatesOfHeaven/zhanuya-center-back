from pydantic import BaseModel
from typing import Generic, TypeVar
from abc import ABC, abstractmethod


T = TypeVar('T')


class BaseResponse(BaseModel, ABC):
    @staticmethod
    @abstractmethod
    def to_json(*args, **kwargs):
        pass


class GeneralResponse(BaseResponse):
    detail: str

    @staticmethod
    def to_json(detail: str):
        return GeneralResponse(detail = detail).model_dump()
    

class PaginationResponse(BaseResponse, Generic[T]):
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