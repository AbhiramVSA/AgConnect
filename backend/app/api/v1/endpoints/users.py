# app/api/v1/endpoints/users.py
from fastapi import APIRouter, Depends
from gotrue import User
from app.core.dependencies import get_current_user
from app.schemas.user import UserPublic 

router = APIRouter()

@router.get("/me", response_model=UserPublic)
def read_users_me(current_user: User = Depends(get_current_user)):
    
    return {
        "id": hash(current_user.id), 
        "email": current_user.email
    }