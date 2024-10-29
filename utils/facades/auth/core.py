from jwt import encode, decode
from time import time
from datetime import timedelta


path_to_keys_dir = 'config'
algorithm = 'RS256'
payload_key = 'sub'

with open(f'{path_to_keys_dir}/public-key.pem', 'rb') as file:
    PUBLIC_KEY = file.read()

with open(f'{path_to_keys_dir}/private-key.pem', 'rb') as file:
    PRIVATE_KEY = file.read()
    

def generate_token(id: int) -> str:
    return encode(
        {
            'exp': int(time()) + timedelta(hours = 12).seconds,
            payload_key: id
        },
        PRIVATE_KEY,
        algorithm
    )


def authenticate_token(token: str) -> int:
    return decode(
        token.replace('Bearer ', '').strip(),
        PUBLIC_KEY,
        [algorithm]
    )[payload_key]