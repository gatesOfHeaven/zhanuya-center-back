from pytest import mark
from httpx import AsyncClient
from fastapi import status

from tests.utils.app import anyio_backend, client


@mark.anyio
@mark.parametrize(('doctors', 'categories', 'offices'), [
    (False, False, False),
    (False, False, True),
    (False, True, False),
    (False, True, True),
    (True, False, False),
    (True, False, True),
    (True, True, False),
    (True, True, True)
])
async def test_get_resources(
    doctors: bool,
    categories: bool,
    offices: bool,
    client: AsyncClient,
    anyio_backend
):
    response = await client.get('/patient/resources', params = {
        'doctors': doctors,
        'categories': categories,
        'offices': offices
    })

    response_data: dict[str, list] = response.json()
    doctors_arr: list = response_data['doctors']
    categories_arr: list = response_data['categories']
    offices_arr: list = response_data['offices']

    assert response.status_code == status.HTTP_200_OK
    if not doctors: assert len(doctors_arr) == 0
    if not categories: assert len(categories_arr) == 0
    if not offices: assert len(offices_arr) == 0