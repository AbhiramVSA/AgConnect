from fastapi import FastAPI
from api.v1.api import api_router

app = FastAPI(
    title="AgConnect API",
    description="API for creating and interacting with AI agents.",
    version="1.0.0"
)

app.include_router(api_router, prefix="/api")

@app.get("/", tags=["Root"])
def read_root():
    return {"message": "Welcome to AgConnect API!"}