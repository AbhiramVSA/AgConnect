from fastapi import FastAPI
from app.api.v1.api import api_router

# This is the 'app' instance Uvicorn is looking for
app = FastAPI(
    title="AgConnect API",
    description="API for creating and interacting with AI agents.",
    version="1.0.0"
)

# Include the versioned API router
app.include_router(api_router, prefix="/api")

@app.get("/", tags=["Root"])
def read_root():
    return {"message": "Welcome to AgConnect API!"}