from datetime import date, timedelta


def get_age(birth_date: date) -> int:
    today = date.today()
    age = today.year - birth_date.year

    if (today.month, today.day) < (birth_date.month, birth_date.day):
        age -= 1
    return age


def get_monthes(birth_date: date) -> int:
    today = date.today()
    return (today.year - birth_date.year)*12 + (today.month - birth_date.month)
    