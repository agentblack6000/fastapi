from pydantic import BaseModel, EmailStr, Field


class UserSignup(BaseModel):
    email: EmailStr
    username: str
    password: str = Field(
        ..., min_length=8, description="Password must be atleast 8 characters long"
    )


class UserLogin(BaseModel):
    username: str
    password: str


class UserResponse(BaseModel):
    email: str
    username: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: str | None = None
