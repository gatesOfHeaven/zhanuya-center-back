from pytest import mark
from httpx import AsyncClient, ASGITransport
from fastapi import status
from sqlalchemy.ext.asyncio import AsyncSession

from entities.user import UserQuery, UserAsPrimary
from routes.auth import SignInReq
from tests.utils.app import anyio_backend, client
from tests.utils.db import temp_db


@mark.anyio
async def test_search_doctor(client: AsyncClient, temp_db: AsyncSession, anyio_backend):
    response = await client.get('/doctors')