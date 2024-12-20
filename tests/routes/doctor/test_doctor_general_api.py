from pytest import mark
from httpx import AsyncClient
from fastapi import status
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timedelta

from utils.decorators import auth
from entities.doctor.factory import Factory as DoctorFactory
from entities.worktime import WorktimeQuery
from entities.workday import WorkdayQuery
from entities.slot.factory import Factory as SlotFactory
from routes.doctor import MySchedule
from tests.helpers.app import anyio_backend, client
from tests.helpers.db import temp_db


@mark.anyio
@mark.parametrize(('week_num'), [ 0, 1, 2 ])
async def test_my_schedule(
    week_num: int,
    client: AsyncClient,
    temp_db: AsyncSession,
    anyio_backend
):
    for doctor in await DoctorFactory(temp_db).get_random(10):
        response = await client.get(f'doctor/schedule/{week_num}', headers = auth.get_auth_headers(doctor.profile))

        workdays = await WorkdayQuery(temp_db).get_schedule(doctor, week_num)
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == MySchedule.to_json(
            worktime = await WorktimeQuery(temp_db).get(workdays[0].date) if workdays else None,
            schedule = workdays
        )


@mark.anyio
async def test_medical_record_access(
    client: AsyncClient,
    temp_db: AsyncSession,
    anyio_backend
):
    for doctor in await DoctorFactory(temp_db).get_random(10):
        for appointment in await SlotFactory(temp_db).by_doctor(doctor, 20):
            response = await client.get(
                url = f'doctor/appointments/{appointment.id}/patient/medical-records',
                headers = auth.get_auth_headers(doctor.profile)
            )
            start_datetime = appointment.start_datetime()
            if start_datetime - timedelta(hours = 1) <= datetime.now() <= start_datetime + timedelta(hours = 2):
                assert response.status_code == status.HTTP_200_OK
            else: assert response.status_code == status.HTTP_403_FORBIDDEN