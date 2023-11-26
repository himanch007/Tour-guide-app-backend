from pydantic import BaseModel, EmailStr


class RegisterRequestFormat(BaseModel):
    name: str
    email: EmailStr
    password: str
    reenteredPassword: str
