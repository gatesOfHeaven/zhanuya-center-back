from re import match


def is_email(string: str) -> bool:
    return '@' in string


def is_iin(string: str) -> bool:
    return match(r'^\d{12}$', string)