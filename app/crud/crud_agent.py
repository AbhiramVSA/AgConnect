from supabase import Client
from gotrue import User
from schemas.agent import AgentCreate

def create_agent(db: Client, *, agent_in: AgentCreate, user: User):
    """
    Create a new agent in the database.
    """
    agent_data = agent_in.model_dump()
    agent_data['user_id'] = str(user.id) # Add the user's ID
    
    response = db.table('agents').insert(agent_data).execute()
    return response.data[0]


def get_user_agents(db: Client, *, user: User):
    """
    Get all agents owned by a specific user.
    """
    response = db.table('agents').select('*').eq('user_id', str(user.id)).execute()
    return response.data