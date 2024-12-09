from enum import Enum
from datetime import timedelta


TIMEDELTA_BEFORE_START_TO_CONFIRM = timedelta(minutes = 20)
TIMEDELTA_AFTER_START_TO_CONFIRM = timedelta(minutes = 10)


class AppointmentStatus(str, Enum):
    BOOKED = 'booked'
    MISSED = 'missed'
    OCCUPIED = 'occupied'