# from pytest import mark
# from httpx import AsyncClient
# from fastapi import status
# from sqlalchemy.ext.asyncio import AsyncSession

# from main import app
# from config.app import HOST
# from entities.user import UserQuery, UserAsPrimary
# from entities.user.factory import Factory as UserFactory
# from routes.auth import SignInReq


# @mark.asyncio
# async def test_sign_in(temp_db: AsyncSession):
#     me = (await UserQuery(temp_db).get_random(1))[0]
#     async with AsyncClient(app = app, base_url = f'{HOST}/auth') as client:
#         response = await client.post('', json = SignInReq(
#             login = me.iin,
#             password = me.password # test only
#         ).model_dump())

#         assert response.status_code == status.HTTP_200_OK
#         assert response.json() == UserAsPrimary.to_json(me)