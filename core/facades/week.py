from datetime import date, timedelta


def get_week(part_of_week: date = date.today(), week_num: int = 0) -> list[date]:
    start_of_week = part_of_week - timedelta(days=part_of_week.weekday())
    start_of_week += timedelta(weeks=week_num)
    return [start_of_week + timedelta(days=i) for i in range(7)]