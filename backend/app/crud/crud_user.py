from supabase import Client, PostgrestAPIResponse
from app.schemas.user import UserCreate

def get_user_by_email(db: Client, email: str): 
    response = db.table('users').select('*').eq('email', email).single().execute()
    return response.data

def create_user(db: Client, *, user_in: UserCreate) -> PostgrestAPIResponse:
    user_credentials = { 
        "email": user_in.email, 
        "password": user_in.password 
    }
    
    response = db.auth.sign_up(user_credentials)
    return response
    