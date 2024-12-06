from core.bases import BaseFactory
from .entity import Category


category_titles = [
    'urologist',
    'radiologist',
    'cardiologist',
    'dentist',
    'gynecologist',
    'dermatologist',
    'pediatrician'
]


class Factory(BaseFactory):
    async def seed(self):
        fakes: list[Category] = [
            Category(title = title)
            for title in category_titles
        ]
        await self.flush(fakes)
        return fakes