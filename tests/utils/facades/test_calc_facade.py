# from pytest import mark
# from datetime import date, time, datetime

# from utils.facades import calc


# time_format_str_params = [
#     (date(1999, 2, 3), '%m.%d.%Y', '02.03.1999')
# ]


# @mark.parametrize(('timepoint', 'format', 'time_in_str'), time_format_str_params)
# def test_time_to_str(
#     time_in_time: datetime | date | time,
#     format: str,
#     time_in_str: str
# ):
#     assert calc.time_to_str(timepoint=time_in_time,format= format) == time_in_str


# @mark.parametrize(('timepoint', 'format', 'time_in_str'), time_format_str_params)
# def test_str_to_time(
#     time_in_time: date | time | datetime,
#     format: str,
#     time_in_str: str
# ):
#     assert calc.str_to_time(time_in_str, format) == time_in_time