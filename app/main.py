from fastapi import FastAPI
# Ensure this import does NOT have 'app.' at the beginning
from api.v1.api import api_router

# The variable must be named 'app'
app = FastAPI(
    title="AgConnect API",
    description="API for creating and interacting with AI agents.",
    version="1.0.0"
)

# This router is included in the 'app' instance
app.include_router(api_router, prefix="/api")

@app.get("/", tags=["Root"])
def read_root():
    return {"message": "Welcome to AgConnect API!"}