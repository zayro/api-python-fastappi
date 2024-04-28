from pydantic import BaseModel, Field, EmailStr


class User(BaseModel):
    username: str = Field(min_length=3)
    password: str = Field(min_length=6)
    email: EmailStr | None = Field(default=None)
    id_users: int | None = None


class UserPasswordChange(BaseModel):
    email: EmailStr
    oldPassword: str
    newPassword: str
