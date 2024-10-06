from fastapi import HTTPException, status
from jwt import encode, decode
from time import time


path_to_keys_dir = 'config'

with open(f'{path_to_keys_dir}/public-key.pem', 'rb') as file:
    PUBLIC_KEY = file.read()

with open(f'{path_to_keys_dir}/private-key.pem', 'rb') as file:
    PRIVATE_KEY = file.read()
    

def generate_token(id: int) -> str:
    return encode(
        {
            'exp': int(time()) + 10*60*60,
            'sub': id
        },
        PRIVATE_KEY,
        'RS256'
    )


def authenticate_token(token: str) -> int:
    try:
        return decode(
            token.replace('Bearer ', '').strip(),
            PUBLIC_KEY,
            ['RS256']
        )['sub']
    except:
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED,
            'Invalid Token'
        )