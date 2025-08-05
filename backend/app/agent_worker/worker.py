# app/agent_worker/worker.py
import asyncio
import logging

from livekit.agents import JobContext, WorkerOptions, cli, JobProcess, AgentSession, Agent, RoomInputOptions # Import Agent, AgentSession, RoomInputOptions
from livekit.agents.llm import ChatContext, ChatMessage
from livekit.plugins import deepgram, silero, cartesia, openai, noise_cancellation
from backend.app.core.config import Settings

settings = Settings()

logging.basicConfig(level=logging.INFO)

def prewarm(proc: JobProcess):
    """
    Pre-warms resources before the worker starts accepting jobs.
    This function is called once per process, and it's a good place to load
    models or other resources that are shared across all jobs.
    """
    logging.info("Pre-warming VAD model...")
    try:
        proc.userdata["vad"] = silero.VAD.load()
        logging.info("VAD model loaded successfully.")
    except Exception as e:
        logging.error(f"Failed to load VAD model: {e}")
        exit(1)


class Assistant(Agent):
    def __init__(self, instructions: str) -> None:
        super().__init__(instructions=instructions)

async def entrypoint(ctx: JobContext):
    """
    This is the entrypoint for each new agent job.
    A new job is created for each new call that the agent joins.
    """
    
    prompt = ctx.job.data or "You are a friendly and helpful voice assistant."
    logging.info(f"Starting agent with prompt: {prompt}")

   
    session = AgentSession(
        stt=deepgram.STT(model="nova-2", language="multi", api_key=settings.DEEPGRAM_API_KEY),
        llm=openai.LLM(model="gpt-4o-mini", api_key=settings.OPENAI_API_KEY),
        tts=cartesia.TTS(model="sonic-2", voice="f786b574-daa5-4673-aa0c-cbe3e8534c02", api_key=settings.CARTESIA_API_KEY),
        vad=ctx.proc.userdata["vad"], 
       
    )

   
    agent_instance = Assistant(instructions=prompt) 

    await session.start(
        room=ctx.room,
        agent=agent_instance,
        room_input_options=RoomInputOptions(
            
            noise_cancellation=noise_cancellation.BVC(), 
        ),
    )
    logging.info(f"Agent connected to room: {ctx.room.name}")
    
    #
    logging.info("Generating initial greeting...")
    await session.generate_reply("Greet the user and ask how you can help.", allow_interruptions=True)

    
    await asyncio.Future() 

if __name__ == "__main__":
    cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint, prewarm_fnc=prewarm))