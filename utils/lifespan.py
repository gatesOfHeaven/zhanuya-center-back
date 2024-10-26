from fastapi import FastAPI
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger

from .bases import BaseEntity
from .db import engine


async def notify_about_upcoming_appointments():
    pass


scheduler = AsyncIOScheduler()
scheduler.add_job(
    notify_about_upcoming_appointments,
    IntervalTrigger(minutes = 5)
)


async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(BaseEntity.metadata.create_all)
    scheduler.start()
    yield
    scheduler.shutdown()