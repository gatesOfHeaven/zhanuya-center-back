from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.date import DateTrigger
from apscheduler.job import Job
from datetime import datetime, timedelta
from typing import Callable, Coroutine, TypeVarTuple
from pytz import timezone
from asyncio import run, create_task, sleep
import logging

logging.basicConfig()
logging.getLogger('apscheduler').setLevel(logging.INFO)

scheduler = AsyncIOScheduler(timezone = timezone('Asia/Almaty'))
scheduler.start()

Args = TypeVarTuple('Args')


def later(
    id: str,
    job: Callable[[*Args], Coroutine],
    args: tuple[*Args]
):
    run_time = datetime.now() + timedelta(seconds=10)
    print(f"Current time: {datetime.now()}, Scheduled time: {run_time}")

    job: Job = scheduler.add_job(
        id=id,
        func=create_task,  # Создаём задачу для асинхронной функции
        trigger=DateTrigger(run_date=run_time),
        args=[job(*args)]  # Передаём coroutine как аргумент
    )
    print(f"Job Trigger: {job.trigger}")


def all_jobs():
    print("Scheduled Jobs:")
    for job in scheduler.get_jobs():
        print(f"ID: {job.id}, Args: {job.args}, Trigger: {job.trigger}")


def remove(id: str):
    scheduler.remove_job(id)


# Пример асинхронной задачи
async def example_task(arg1: str, arg2: int):
    print(f"Task executed with arg1: {arg1}, arg2: {arg2} at {datetime.now()}")


# Тестирование
if __name__ == "__main__":
    # Добавляем задачу
    later("test_job", example_task, ("Hello", 42))

    # Выводим все задачи
    all_jobs()

    # Запускаем событийный цикл
    run(create_task(sleep(15)))  # Даем планировщику время выполнить задачу
