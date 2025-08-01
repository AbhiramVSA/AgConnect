# app/api/v1/endpoints/users.py
from fastapi import APIRouter, Depends
from gotrue import User
from core.dependencies import get_current_user
from schemas.user import UserPublic # We'll use this to format the response

router = APIRouter()

@router.get("/me", response_model=UserPublic)
def read_users_me(current_user: User = Depends(get_current_user)):
    
    return {
        "id": hash(current_user.id), 
        "email": current_user.email
    }