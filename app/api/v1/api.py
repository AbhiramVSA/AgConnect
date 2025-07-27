from fastapi import APIRouter
from .endpoints import auth, users, agents

# This creates the router for version 1
api_router = APIRouter(prefix="/v1")

api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])

api_router.include_router(users.router, prefix="/users", tags=["Users"])

api_router.include_router(agents.router, prefix="/agents", tags=["Agents"])

@api_router.get("/health", tags=["Health"])
def health_check():
    return {"status": "ok"}