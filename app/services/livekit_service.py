# app/services/livekit_service.py
import livekit
from livekit.api import LiveKitAPI, CreateRoomRequest, DispatchJobRequest

from core.config import settings

def create_access_token(room_name: str, participant_identity: str) -> str:
    """
    Generates a LiveKit access token for a participant.
    This function remains the same as it's part of the core SDK.
    """
    access_token = (
        livekit.AccessToken(settings.LIVEKIT_API_KEY, settings.LIVEKIT_API_SECRET)
        .with_identity(participant_identity)
        .with_name(participant_identity)
        .with_grant(livekit.VideoGrant(room=room_name))
    )
    return access_token.to_jwt()

async def dispatch_agent_job(room_name: str, agent_prompt: str, agent_id: int):
    """
    Dispatches a job to an available agent worker to join a room
    using the correct livekit-api client.
    """
    # This will automatically read LIVEKIT_URL, LIVEKIT_API_KEY, and LIVEKIT_API_SECRET
    # from the environment variables loaded by our config.
    async with LiveKitAPI() as lkapi:
        try:
            # Check if the room exists. This will raise an error if not found.
            await lkapi.room.list_rooms(room_names=[room_name])
        except Exception:
            # If the room doesn't exist, create it.
            await lkapi.room.create_room(CreateRoomRequest(name=room_name))

        # Dispatch the job to the agent worker pool
        await lkapi.job.dispatch_job(DispatchJobRequest(
            room=room_name,
            participant_identity=f"agent-{agent_id}",
            data=agent_prompt,
        ))