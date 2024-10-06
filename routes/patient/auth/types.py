from pydantic import BaseModel, Field

from entities.user import User


class SendVerificationReq(BaseModel):
    email: str = Field(pattern=r'[^@]+@[^@]+\.[^@]+')


class SignUpReq(BaseModel):
    name: str = Field(max_length=25)
    surname: str = Field(max_length=25)
    email: str = Field(pattern=r'[^@]+@[^@]+\.[^@]+')
    gender: str = Field(min_length=4, max_length = 6)
    birthDate: str = Field(min_length=10, max_length=10)
    emailVerificationCode: int
    password: str =Field(min_length=8, max_length=25, pattern=r'^[A-Za-z\d@$!%*?&]+$')


class SignUpRes(BaseModel):
    id: int

    def to_json(user: User):
        return SignUpRes(id = user.id).model_dump()