from pytest import mark, fixture
from httpx import AsyncClient
from fastapi import status
from sqlalchemy.ext.asyncio import AsyncSession

from entities.doctor import DoctorAsPrimary
from entities.doctor.factory import Factory as DoctorFactory
from entities.worktime import WorktimeQuery
from entities.workday import WorkdayQuery
from routes.patient.doctors import DoctorAsElement, ScheduleRes
from tests.helpers.app import anyio_backend, client
from tests.helpers.db import temp_db


@fixture
def route_doctors() -> str:
    return '/patient/doctors'


@mark.anyio
async def test_search_doctor(
    client: AsyncClient,
    route_doctors: str,
    temp_db: AsyncSession,
    anyio_backend
):
    for doctor in await DoctorFactory(temp_db).get_random(10):
        name = doctor.profile.name
        surname = doctor.profile.surname
        for fullname in [f'{name} {surname}', f'{surname} {name}']:
            response = await client.get(route_doctors, params = { 'fullname': fullname })
            response_data = [DoctorAsElement(**doctor) for doctor in response.json()]

            assert response.status_code == status.HTTP_200_OK
            assert len(response_data) == 1
            assert response_data[0].model_dump() == DoctorAsElement.to_json(doctor)


@mark.anyio
async def test_doctor_profile(
    client: AsyncClient,
    route_doctors: str,
    temp_db: AsyncSession,
    anyio_backend
):
    for doctor in await DoctorFactory(temp_db).get_random(10):
        response = await client.get(f'{route_doctors}/{doctor.id}')
        response_data = DoctorAsPrimary(**response.json())

        assert response.status_code == status.HTTP_200_OK
        assert response_data.model_dump() == DoctorAsPrimary.to_json(doctor)


@mark.anyio
async def test_doctor_schedule(
    client: AsyncClient,
    route_doctors: str,
    temp_db: AsyncSession,
    anyio_backend
):
    for doctor in await DoctorFactory(temp_db).get_random(10):
        for week_num in range(3):
            response = await client.get(f'{route_doctors}/{doctor.id}/{week_num}')
            response_data = ScheduleRes(**response.json())

            assert response.status_code == status.HTTP_200_OK
            workdays = await WorkdayQuery(temp_db).get_schedule(doctor, week_num)
            assert response_data.model_dump() == ScheduleRes.to_json(
                worktime = await WorktimeQuery(temp_db).get(workdays[0].date) if workdays else None,
                schedule = workdays,
                me = None
            )