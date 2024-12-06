from datetime import date, time, datetime, timedelta


def str_to_time(str_time: str, format: str) -> datetime:
    return datetime.strptime(str_time, format)


def time_to_str(
    timepoint: datetime | date | time,
    format: str = '%d.%m.%Y'
) -> str:
    return timepoint.strftime(format)


def add_times(init_time: time, delta: timedelta) -> time:
    return (datetime.combine(date.today(), init_time) + delta).time()


def get_age(birth_date: date) -> int:
    today = date.today()
    age = today.year - birth_date.year

    if (today.month, today.day) < (birth_date.month, birth_date.day):
        age -= 1
    return age


def get_monthes(birth_date: date) -> int:
    today = date.today()
    return (today.year - birth_date.year)*12 + (today.month - birth_date.month)