from pydantic import BaseModel

from .entity import Category


class CategoryAsForeign(BaseModel):
    id: int
    title: str

    def to_json(category: Category):
        return CategoryAsForeign(
            id = category.id,
            title = category.title
        ).model_dump()