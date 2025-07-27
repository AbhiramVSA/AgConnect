# app/api/v1/endpoints/agents.py
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from supabase import Client
from gotrue import User

# Corrected imports to be direct and avoid loops
from schemas.agent import AgentCreate, AgentPublic
from crud import crud_agent
from services.supabase_client import get_supabase_client
from core.dependencies import get_current_user

router = APIRouter()

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