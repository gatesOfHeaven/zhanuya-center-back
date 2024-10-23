from pytest import mark
from httpx import AsyncClient
from fastapi import status
from sqlalchemy.ext.asyncio import AsyncSession

from entities.user import UserQuery, UserAsPrimary
from routes.auth import SignInReq
from tests.utils.app import anyio_backend, client
from tests.utils.db import temp_db


@mark.anyio
async def test_sign_in_by_iin(client: AsyncClient, temp_db: AsyncSession, anyio_backend):
    for user in await UserQuery(temp_db).get_random(10):
        response = await client.post('/auth', json = SignInReq(
            login = user.iin,
            password = user.password # test only
        ).model_dump())

        assert response.status_code == status.HTTP_200_OK
        assert response.json() == UserAsPrimary.to_json(user)


@mark.anyio
async def test_sign_in_by_email(client: AsyncClient, temp_db: AsyncSession, anyio_backend):
    for user in await UserQuery(temp_db).get_random(10):
        response = await client.post('/auth', json = SignInReq(
            login = user.email,
            password = user.password # test only
        ).model_dump())

        assert response.status_code == status.HTTP_200_OK
        assert response.json() == UserAsPrimary.to_json(user)