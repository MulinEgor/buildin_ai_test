from pydantic import BaseModel, EmailStr

    
class UserResponseSchema(BaseModel):
    uuid: str
    email: EmailStr


class TokenResponseSchema(BaseModel):
    access_token: str
    refresh_token: str

    
class UserTokenResponseSchema(UserResponseSchema, TokenResponseSchema):
    pass
    
