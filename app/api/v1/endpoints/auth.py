from fastapi import APIRouter, Depends, HTTPException, status
from supabase import Client, PostgrestAPIResponse
from schemas.user import UserCreate
from models.token import Token
from crud import crud_user
from services.supabase_client import get_supabase_client

router = APIRouter()

@router.post("/register", status_code=status.HTTP_201_CREATED)
def register_user(*, db: Client = Depends(get_supabase_client), user_in: UserCreate):
    response: PostgrestAPIResponse = crud_user.create_user(db=db, user_in=user_in)
    
    if response.user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Could not register user. Email may already be in use."
        )

    return {"message": "Registration successful. Please check your email to verify your account."}

@router.post("/login", response_model=Token)
def login_for_access_token(*, db: Client = Depends(get_supabase_client), user_in: UserCreate):
    
    try:
        response = db.auth.sign_in_with_password({
            "email": user_in.email,
            "password": user_in.password
        })

        access_token = response.session.access_token
        return {
            "access_token": access_token,
            "token_type": "bearer",
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )