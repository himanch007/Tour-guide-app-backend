from pydantic import BaseModel, EmailStr, validator
from users.models.managers.user import UserManager


class User(BaseModel):
    name: str
    email: EmailStr
    password: str
    metadata: dict

    @validator('name')
    def name_is_required(cls, v):
        if v == '':
            raise ValueError('name is required')
        return v

    @validator('password')
    def password_is_required(cls, v):
        if v == '':
            raise ValueError('password is required')
        return v

    class Model:
        name = 'User'
        objects = UserManager()
