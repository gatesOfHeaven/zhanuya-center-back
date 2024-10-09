from utils.bases import BaseFactory
from .entity import Role


role_names = [
    'pateint',
    'doctor',
    'manager'
]


class Factory(BaseFactory):
    fakes: list[Role]

    async def seed(self):
        self.fakes = []

        for name in role_names:
            role = Role(name = name)
            self.fakes.append(role)
            self.db.add(role)
        await self.flush()
        return self.fakes