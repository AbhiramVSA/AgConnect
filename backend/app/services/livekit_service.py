# app/services/livekit_service.py
import livekit
from livekit.api import LiveKitAPI, CreateRoomRequest
from livekit.api.access_token import AccessToken
from app.core.config import Settings

settings = Settings()

def create_access_token(room_name: str, participant_identity: str) -> str:
    """
    Generates a LiveKit access token for a participant.
    """
    access_token = (
        AccessToken(settings.LIVEKIT_API_KEY, settings.LIVEKIT_API_SECRET)
        .with_identity(participant_identity)
        .with_name(participant_identity)
        .with_grant(livekit.VideoGrant(room=room_name))
    )
    return access_token.to_jwt()

async def dispatch_agent_job(room_name: str, agent_prompt: str, agent_id: int):
    """
    Dispatches a job to an available agent worker to join a room.
    """
    async with LiveKitAPI() as lkapi:
  
        response = await lkapi.room.list_rooms(names=[room_name])
        
        
        if not response.rooms:
            
            await lkapi.room.create_room(CreateRoomRequest(name=room_name))

        
        await lkapi.agent_dispatch.dispatch(
            type=livekit.JobType.JT_ROOM,
            room=room_name,
            participant_identity=f"agent-{agent_id}",
            data=agent_prompt, 
        )