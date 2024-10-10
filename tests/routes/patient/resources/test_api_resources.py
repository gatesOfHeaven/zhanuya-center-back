# from pytest import mark
# from httpx import AsyncClient
# from fastapi import status

# from main import app
# from config.app import HOST


# @mark.asyncio
# @mark.parametrize(('doctors', 'categories', 'offices'), [
#     (False, False, False),
#     (False, False, True),
#     (False, True, False),
#     (False, True, True),
#     (True, False, False),
#     (True, False, True),
#     (True, True, False),
#     (True, True, True)
# ])
# async def test_get_resources(doctors: bool, categories: bool, offices: bool):
    
#     async with AsyncClient(app = app, base_url = f'{HOST}/resources') as client:
#         response = await client.get('', params = {
#             'doctors': doctors,
#             'categories': categories,
#             'offices': offices
#         })

#         response_data: dict[str, list] = response.json()
#         doctors_arr: list = response_data['doctors']
#         categories_arr: list = response_data['categories']
#         offices_arr: list = response_data['offices']

#         assert response.status_code == status.HTTP_200_OK
#         if not doctors: assert len(doctors_arr) == 0
#         if not categories: assert len(categories_arr) == 0
#         if not offices: assert len(offices_arr) == 0
        
