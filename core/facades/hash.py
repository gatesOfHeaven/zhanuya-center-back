from hashlib import sha256


def it(text_to_hash: str) -> str:
    return sha256(text_to_hash.encode()).hexdigest()