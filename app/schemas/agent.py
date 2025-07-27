from pydantic import BaseModel
from uuid import UUID

class AgentCreate(BaseModel):
    name: str
    prompt: str

class AgentPublic(AgentCreate):
    id: int
    user_id: UUID

    class Config:
        from_attributes = True