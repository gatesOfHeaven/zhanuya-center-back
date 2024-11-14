from enum import Enum

class Role(Enum):
    PATIENT = 'patient'
    DOCTOR = 'doctor'
    MANAGER = 'manager'


class Gender(Enum):
    MALE = 'male'
    FEMALE = 'female'