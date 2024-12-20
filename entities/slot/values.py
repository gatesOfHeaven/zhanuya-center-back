from enum import Enum
from datetime import timedelta


TIMEDELTA_BEFORE_START_TO_CONFIRM = timedelta(minutes = 20)
TIMEDELTA_AFTER_START_TO_CONFIRM = timedelta(minutes = 20)


class AppointmentStatus(str, Enum):
    BOOKED = 'booked'
    MISSED = 'missed'
    CONFIRMED = 'confirmed'


class TimeStatus(str, Enum):
    PAST = 'past'
    UPCOMING = 'upcoming'