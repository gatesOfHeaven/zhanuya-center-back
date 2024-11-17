from pydantic import BaseModel, Field

from utils.bases import BaseResponse
from entities.user import User, Gender


class SendVerificationReq(BaseModel):
    email: str = Field(pattern=r'[^@]+@[^@]+\.[^@]+')
    iin: str = Field(min_length = 12, max_length = 12, pattern = r'^\d+$')


class VerificationConflictElement(BaseModel):
    detail: str
    location: str


class SignUpReq(BaseModel):
    name: str = Field(max_length = 25)
    surname: str = Field(max_length = 25)
    email: str = Field(pattern = r'[^@]+@[^@]+\.[^@]+')
    iin: str = Field(min_length = 12, max_length = 12, pattern = r'^\d+$')
    gender: Gender
    birthDate: str = Field(pattern = r'\d{2}\-\d{2}\-\d{4}')
    emailVerificationCode: int
    password: str =Field(min_length = 8, max_length = 25, pattern = r'^[A-Za-z\d@$!%*?&]+$')


class SignUpRes(BaseResponse):
    id: int

    @staticmethod
    def to_json(user: User):
        return SignUpRes(id = user.id).model_dump()