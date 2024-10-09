from utils.bases import BaseFactory
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
    fakes: list[Category]

    async def seed(self):
        self.fakes = []
        
        for title in category_titles:
            category = Category(title = title)
            self.fakes.append(category)
            self.db.add(category)
        await self.flush()
        return self.fakes