from pytest import mark
from httpx import AsyncClient, ASGITransport
from logging import Logger

from fastapi import status
from sqlalchemy.ext.asyncio import AsyncSession

from main import app
from config.app import HOST
from entities.user import UserQuery, UserAsPrimary
from entities.user.factory import Factory as UserFactory
from routes.auth import SignInReq
from tests.utils.app import anyio_backend, logger
from tests.utils.db import temp_db


@mark.anyio
async def test_sign_in_by_iin(temp_db: AsyncSession, logger: Logger, anyio_backend):
    me = (await UserQuery(temp_db).get_random(1))[0]
    async with AsyncClient(
        transport = ASGITransport(app),
        base_url = HOST
    ) as client:
        response = await client.post('/auth', json = SignInReq(
            login = me.iin,
            password = me.password # test only
        ).model_dump())
        logger.info(f'{response.request.method} {response.request.url}')

        assert response.status_code == status.HTTP_200_OK
        assert response.json() == UserAsPrimary.to_json(me)


@mark.anyio
async def test_sign_in_by_email(temp_db: AsyncSession, logger: Logger, anyio_backend):
    me = (await UserQuery(temp_db).get_random(1))[0]
    async with AsyncClient(
        transport = ASGITransport(app),
        base_url = HOST
    ) as client:
        response = await client.post('/auth', json = SignInReq(
            login = me.email,
            password = me.password # test only
        ).model_dump())
        logger.info(f'{response.request.method} {response.request.url}')

        assert response.status_code == status.HTTP_200_OK
        assert response.json() == UserAsPrimary.to_json(me)