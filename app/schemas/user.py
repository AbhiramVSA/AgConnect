from pydantic import BaseModel, EmailStr, Field

class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8)

class UserPublic(BaseModel):
    id: int  
    email: EmailStr

    class Config:
        from_attributes = True 