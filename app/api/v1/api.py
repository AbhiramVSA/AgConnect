from fastapi import APIRouter
# We will import the actual endpoint files here later, like auth.py or agents.py
# For example: from .endpoints import auth

# This creates the router for version 1
api_router = APIRouter(prefix="/v1")

# This is where we will include other routers
# For example: api_router.include_router(auth.router)


# A simple health check to confirm the router is working
@api_router.get("/health", tags=["Health"])
def health_check():
    """Simple health check endpoint."""
    return {"status": "ok"}