from utils.bases import BaseFactory
from .entity import Role


role_names = [
    'pateint',
    'doctor',
    'manager'
]


class Factory(BaseFactory):
    async def seed(self):
        fakes: list[Role] = [
            Role(name = name)
            for name in role_names
        ]
        await self.flush(fakes)
        return fakes