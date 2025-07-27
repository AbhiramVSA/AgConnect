from fastapi import APIRouter
# Import your endpoint routers here later
# from .endpoints import auth, agents, chats

api_router = APIRouter(prefix="/v1")

# Include your endpoint routers here
# api_router.include_router(auth.router, tags=["Authentication"])
# api_router.include_router(agents.router, tags=["Agents"])
# api_router.include_router(chats.router, tags=["Chats"])

@api_router.get("/health", tags=["Health"])
def health_check():
    """Simple health check endpoint."""
    return {"status": "ok"}