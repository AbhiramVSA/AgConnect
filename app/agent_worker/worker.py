# app/agent_worker/worker.py
import logging
from livekit import agents
from livekit.agents import Agent, AgentSession, JobContext, RoomInputOptions
from livekit.plugins import openai, noise_cancellation

# Configure logging
logging.basicConfig(level=logging.INFO)

class Assistant(Agent):
    """
    This is a simple agent that will use the instructions
    passed to it from the job dispatch.
    """
    def __init__(self, instructions: str):
        super().__init__(instructions=instructions)

async def entrypoint(ctx: JobContext):
    """
    This entrypoint is called when the worker receives a job.
    It creates and starts a real-time AI assistant in the room.
    """
    # Get the agent's instructions from the job data, with a fallback default.
    instructions = ctx.job.data or "You are a friendly and helpful voice assistant."

    session = AgentSession(
        llm=openai.realtime.RealtimeModel(
            # You can customize the voice here
            voice="coral"
        )
    )

    await session.start(
        room=ctx.room,
        agent=Assistant(instructions=instructions),
        room_input_options=RoomInputOptions(
            # Using LiveKit's built-in noise cancellation for clarity
            noise_cancellation=noise_cancellation.BVC(),
        ),
    )

    # The agent will automatically start listening and responding.
    # We can send an initial message to get the conversation started.
    await session.generate_reply(
        instructions="Greet the user and ask how you can help."
    )


if __name__ == "__main__":
    # This is the main entry point for the worker process.
    agents.cli.run_app(agents.WorkerOptions(entrypoint_fnc=entrypoint))