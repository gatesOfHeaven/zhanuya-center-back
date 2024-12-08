from fastapi import FastAPI
from contextlib import asynccontextmanager
from aiofiles import open as asyncopen
from datetime import datetime

from config.rootdir import  LOG_DIR
from core import engine, asyncSession
from core.bases import BaseEntity
from .decorators import exec
from entities.slot import SlotQuery


@asynccontextmanager
async def lifespan(app: FastAPI):
    logs: list[str] = []

    exec.start()
    async with engine.begin() as conn:
        await conn.run_sync(BaseEntity.metadata.create_all)
    async with asyncSession() as db:
        upcoming_appointments = await SlotQuery(db).upcomings()
        for appointment in upcoming_appointments:
            exec.schedule_appointment_notification(appointment, save_log = False)
            logs.append(f'{datetime.now()}: {appointment.id}')
    async with asyncopen(LOG_DIR / 'scheduled-appointments.txt', 'w') as file:
        await file.write('\n'.join(logs))
        
    logs.clear()
    yield