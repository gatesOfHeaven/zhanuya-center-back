from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from utils import engine, asyncSession
from utils.bases import BaseEntity

from entities.worktime import Worktime
from entities.user import User
from entities.email_verification import EmailVerification
from entities.category import Category
from entities.building import Building
from entities.room import Room
from entities.doctor import Doctor
from entities.manager import Manager
from entities.terminal import Terminal
from entities.appointment_type import AppointmentType
from entities.price import Price
from entities.education_record import EducationRecord
from entities.experience_record import ExperienceRecord
from entities.workday import Workday
from entities.lunch import Lunch
from entities.slot import Slot
from entities.payment import Payment
from entities.medical_record import MedicalRecord

from entities.worktime.factory import Factory as WorktimeFactory
from entities.user.factory import Factory as UserFactory
from entities.email_verification.factory import Factory as EmailVerificationFactory
from entities.category.factory import Factory as CategoryFactory
from entities.building.factory import Factory as BuildingFactory
from entities.room.factory import Factory as RoomFactory
from entities.doctor.factory import Factory as DoctorFactory
from entities.manager.factory import Factory as ManagerFactory
from entities.terminal.factory import Factory as TerminalFactory
from entities.appointment_type.factory import Factory as AppointmentTypeFactory
from entities.price.factory import Factory as PriceFactory
from entities.education_record.factory import Factory as EducationRecordFactory
from entities.experience_record.factory import Factory as ExperienceRecordFactory
from entities.workday.factory import Factory as WorkdayFactory
from entities.lunch.factory import Factory as LunchFactory
from entities.slot.factory import Factory as SlotFactory
from entities.payment.factory import Factory as PaymentFactory
from entities.medical_record.factory import Factory as MedicalRecordFactory


async def seed(db: AsyncSession):
    worktimes = await WorktimeFactory(db).seed()
    users = await UserFactory(db).seed(150)
    await EmailVerificationFactory(db).seed(users)
    categories = await CategoryFactory(db).seed()
    buildings = await BuildingFactory(db).seed(1)
    rooms = await RoomFactory(db).seed(25, buildings)
    doctors = await DoctorFactory(db).seed(users, categories, rooms)
    managers = await ManagerFactory(db).seed(users, buildings)
    terminals = await TerminalFactory(db).seed(10, buildings)
    appointment_types = await AppointmentTypeFactory(db).seed()
    prices = await PriceFactory(db).seed(doctors, appointment_types)
    await EducationRecordFactory(db).seed(doctors, managers)
    await ExperienceRecordFactory(db).seed(doctors, managers, categories)
    workdays = await WorkdayFactory(db).seed(worktimes, doctors)
    await LunchFactory(db).seed(workdays)
    slots = await SlotFactory(db).seed(workdays, users, prices)
    await PaymentFactory(db).seed(slots, managers, terminals, 80, 70)
    await MedicalRecordFactory(db).seed(slots, managers)


async def main():
    async with engine.begin() as conn:
        await conn.run_sync(BaseEntity.metadata.drop_all)
        await conn.run_sync(BaseEntity.metadata.create_all)
    
    async with asyncSession() as db:
        db: AsyncSession
        try:
            await seed(db)
            await db.commit()
        except SQLAlchemyError as e:
            await db.rollback()
            print(e)


if __name__ == '__main__':
    from asyncio import run
    run(main())