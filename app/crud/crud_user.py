from supabase import Client, PostgrestAPIResponse
from schemas.user import UserCreate

def get_user_by_email(db: Client, emial: str):
    
    pass


def create_user(db: Client, *, user_in: UserCreate) -> PostgrestAPIResponse:
    
    user_credentials = { 
        "email": user_in.email, 
        "password": user_in.password 
    }
    
    response = db.auth.sign_up(user_credentials)
    return response
    