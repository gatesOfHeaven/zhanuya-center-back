from fastapi import FastAPI
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from datetime import datetime

from .bases import BaseEntity
from .db import engine, asyncSession
from .facades import exec
from entities.slot import SlotQuery


async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(BaseEntity.metadata.create_all)
    # async with asyncSession() as db:
    #     upcoming_appointments = await SlotQuery(db).upcomings()
    #     print(len(upcoming_appointments))
    #     for appointment in upcoming_appointments:
    #         exec.unschedule_appointment_notification(appointment)
    #         exec.schedule_appointment_notification(appointment)
    yield