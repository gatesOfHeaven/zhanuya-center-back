from pydantic import BaseModel, Field


class SignInReq(BaseModel):
    email: str = Field(pattern=r'[^@]+@[^@]+\.[^@]+')
    password: str =Field(min_length=8, max_length=25, pattern=r'^[A-Za-z\d@$!%*?&]+$')