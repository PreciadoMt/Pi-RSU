from pydantic import BaseModel, EmailStr

class ModelLogin(BaseModel):
    email: EmailStr
    password: str

class ModelToken(BaseModel):
    access_token: str
    token_type: str