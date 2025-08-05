# app/api/v1/endpoints/agents.py
import asyncio
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from supabase import Client
from gotrue import User
from pydantic import BaseModel

from app.schemas.agent import AgentCreate, AgentPublic
from app.crud import crud_agent
from app.services import livekit_service
from app.services.supabase_client import get_supabase_client
from app.core.dependencies import get_current_user

router = APIRouter()

class JoinCallResponse(BaseModel):
    token: str


@router.post("/", response_model=AgentPublic, status_code=status.HTTP_201_CREATED)
def create_new_agent(
    *,
    db: Client = Depends(get_supabase_client),
    current_user: User = Depends(get_current_user),
    agent_in: AgentCreate
):
    """
    Create a new AI agent for the current user.
    """
    agent = crud_agent.create_agent(db=db, agent_in=agent_in, user=current_user)
    return agent

@router.get("/", response_model=List[AgentPublic])
def read_user_agents(
    *,
    db: Client = Depends(get_supabase_client),
    current_user: User = Depends(get_current_user)
):
    """
    Retrieve all agents for the current user.
    """
    agents = crud_agent.get_user_agents(db=db, user=current_user)
    return agents

@router.post("/{agent_id}/join-call", response_model=JoinCallResponse)
async def join_agent_call(
    agent_id: int,
    db: Client = Depends(get_supabase_client),
    current_user: User = Depends(get_current_user),
):
    """
    Generates a LiveKit token for the user AND dispatches the AI agent to the call.
    """
 
    agent_record = (
        db.table('agents')
        .select('prompt')
        .eq('id', agent_id)
        .eq('user_id', str(current_user.id)) # Check ownership
        .single()
        .execute()
    )

    if not agent_record.data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Agent not found or you do not have permission to access it."
        )

    agent_prompt = agent_record.data['prompt']

    room_name = f"agent-call-{agent_id}"
    participant_identity = str(current_user.id)

    user_token = livekit_service.create_access_token(
        room_name=room_name, participant_identity=participant_identity
    )

    # Dispatch the agent to the call
    await livekit_service.dispatch_agent_job(
        room_name=room_name, agent_prompt=agent_prompt, agent_id=agent_id
    )
    
    return {"token": user_token}