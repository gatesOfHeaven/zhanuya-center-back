from pytest import mark, fixture
from httpx import AsyncClient
from fastapi import status
from sqlalchemy.ext.asyncio import AsyncSession

from entities.doctor import DoctorQuery, DoctorAsPrimary
from entities.worktime import WorktimeQuery
from entities.workday import WorkdayQuery
from routes.patient.doctors import DoctorAsElement, ScheduleRes
from tests.utils.app import anyio_backend, client
from tests.utils.db import temp_db


@fixture
def route() -> str:
    return '/patient/doctors'


@mark.anyio
async def test_search_doctor(
    client: AsyncClient,
    route: str,
    temp_db: AsyncSession,
    anyio_backend
):
    for doctor in await DoctorQuery(temp_db).get_random(10):
        name = doctor.profile.name
        surname = doctor.profile.surname
        for fullname in [f'{name} {surname}', f'{surname} {name}']:
            response = await client.get(route, params = { 'fullname': fullname })
            response_data: list[DoctorAsElement] = response.json()

            assert response.status_code == status.HTTP_200_OK
            assert len(response_data) == 1
            assert response_data[0] == DoctorAsElement.to_json(doctor)


@mark.anyio
async def test_doctor_profile(
    client: AsyncClient,
    route: str,
    temp_db: AsyncSession,
    anyio_backend
):
    for doctor in await DoctorQuery(temp_db).get_random(10):
        response = await client.get(f'{route}/{doctor.id}')
        response_data: DoctorAsPrimary = response.json()

        assert response.status_code == status.HTTP_200_OK
        assert response_data == DoctorAsPrimary.to_json(doctor)


@mark.anyio
async def test_doctor_schedule(
    client: AsyncClient,
    route: str,
    temp_db: AsyncSession,
    anyio_backend
):
    for doctor in await DoctorQuery(temp_db).get_random(10):
        for week_num in range(3):
            response = await client.get(f'{route}/{doctor.id}/{week_num}')
            response_data: ScheduleRes = response.json()

            assert response.status_code == status.HTTP_200_OK
            assert response_data == ScheduleRes.to_json(
                worktime = await WorktimeQuery(temp_db).get_actual(),
                schedule = await WorkdayQuery(temp_db).get_schedule(
                    doctor = doctor,
                    week_num = week_num
                ),
                me = None
            )