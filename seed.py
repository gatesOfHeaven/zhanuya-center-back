from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import date

from utils.db import engine, asyncSession
from utils.bases import BaseEntity
from entities.worktime.factory import Factory as WorktimeFactory
from entities.role.factory import Factory as RoleFactory
from entities.user.factory import Factory as UserFactory
from entities.email_verification.factory import Factory as EmailVerificationFactory
from entities.category.factory import Factory as CategoryFactory
from entities.building.factory import Factory as BuildingFactory
from entities.room.factory import Factory as RoomFactory
from entities.doctor.factory import Factory as DoctorFactory
from entities.workday.factory import Factory as WorkdayFactory
from entities.slot.factory import Factory as SlotFactory


async def seed():
    async with engine.begin() as conn:
        metadata: MetaData = BaseEntity.metadata
        await conn.run_sync(metadata.create_all)
    
    async with asyncSession() as db:
        db: AsyncSession
        worktimes = await WorktimeFactory(db).seed()
        roles = await RoleFactory(db).seed()
        users = await UserFactory(db).seed(100, roles)
        await EmailVerificationFactory(db).seed(users)
        categories = await CategoryFactory(db).seed()
        buildings = await BuildingFactory(db).seed(3)
        rooms = await RoomFactory(db).seed(25, buildings)
        doctors = await DoctorFactory(db).seed(users, categories, rooms)
        workdays = await WorkdayFactory(db).seed(date(2024, 9, 30), worktimes, doctors)
        await SlotFactory(db).seed(workdays, users)
        await db.commit()


if __name__ == '__main__':
    from asyncio import run
    run(seed())