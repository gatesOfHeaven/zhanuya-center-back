from pytest import mark
from httpx import AsyncClient
from fastapi import status
from sqlalchemy.ext.asyncio import AsyncSession

from entities.user import Role, UserAsPrimary
from entities.user.factory import Factory as UserFactory
from routes.auth import SignInReq
from tests.helpers.app import anyio_backend, client
from tests.helpers.db import temp_db


@mark.anyio
@mark.parametrize(('role'), [Role.PATIENT, Role.DOCTOR, Role.MANAGER])
async def test_sign_in_by_iin(role: Role, client: AsyncClient, temp_db: AsyncSession, anyio_backend):
    for user in await UserFactory(temp_db).get_random(10, role):
        response = await client.post('/auth', json = SignInReq(
            login = user.iin,
            password = user.password # test only
        ).model_dump())

        assert response.status_code == status.HTTP_200_OK
        assert response.json() == UserAsPrimary.to_json(user)


@mark.anyio
@mark.parametrize(('role'), [Role.PATIENT, Role.DOCTOR, Role.MANAGER])
async def test_sign_in_by_email(role: Role, client: AsyncClient, temp_db: AsyncSession, anyio_backend):
    for user in await UserFactory(temp_db).get_random(10, role):
        response = await client.post('/auth', json = SignInReq(
            login = user.email,
            password = user.password # test only
        ).model_dump())

        assert response.status_code == status.HTTP_200_OK
        assert response.json() == UserAsPrimary.to_json(user)