from re import match


def is_email(string: str) -> bool:
    return match(
        r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$',
        string
    )


def is_iin(string: str) -> bool:
    return match(r'^\d{12}$', string)