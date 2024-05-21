from pydantic import BaseModel, Field, EmailStr


class User(BaseModel):
    id_users: int = Field(default=None, primary_key=True)
    username: str = Field(min_length=3)
    password: str = Field(min_length=6)
    email: EmailStr | None = Field(default=None)


class UserLogin(BaseModel):
    username: str
    password: str


class UserPasswordChange(BaseModel):
    email: EmailStr
    oldPassword: str
    newPassword: str
