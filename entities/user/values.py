from enum import Enum

class Role(str, Enum):
    PATIENT = 'patient'
    DOCTOR = 'doctor'
    MANAGER = 'manager'


class Gender(str, Enum):
    MALE = 'male'
    FEMALE = 'female'