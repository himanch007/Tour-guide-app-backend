from pydantic import BaseModel, EmailStr


class LoginRequestFormat(BaseModel):
    email: EmailStr
    password: str