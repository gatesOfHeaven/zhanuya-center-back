from fastapi import FastAPI
from contextlib import asynccontextmanager

from core import engine, asyncSession
from core.bases import BaseEntity
from .decorators import exec
from entities.slot import SlotQuery


@asynccontextmanager
async def lifespan(app: FastAPI):
    exec.start()
    async with engine.begin() as conn:
        await conn.run_sync(BaseEntity.metadata.create_all)
    async with asyncSession() as db:
        upcoming_appointments = await SlotQuery(db).upcomings()
        for appointment in upcoming_appointments:
            exec.schedule_appointment_notification(appointment)
            print(appointment.id, 'scheduled')
    yield