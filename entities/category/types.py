from utils.bases import BaseResponse

from .entity import Category


class CategoryAsForeign(BaseResponse):
    id: int
    title: str

    @staticmethod
    def to_json(category: Category):
        return CategoryAsForeign(
            id = category.id,
            title = category.title
        ).model_dump()