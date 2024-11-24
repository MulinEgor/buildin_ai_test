from pydantic import BaseModel, EmailStr


class UserRequestSchema(BaseModel):
    email: EmailStr
    password: str


class UserHashedPasswordRequestSchema(BaseModel):
    email: EmailStr
    hashed_password: str
