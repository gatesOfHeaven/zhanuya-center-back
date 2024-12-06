from pytest import mark

from core.facades import auth


@mark.parametrize(('id'), [(1), (2), (0), (-1), (10**10), (-1 * 10**10)])
def test_token_generation(id: int):
    token = auth.generate_token(id)
    assert id == auth.authenticate_token(token)