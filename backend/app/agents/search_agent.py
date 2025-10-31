from pathlib import Path

from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.openai import OpenAIProvider

from config.config import settings

BASE_DIR = Path(__file__).resolve().parent
PROMPTS_DIR = BASE_DIR.parent / "prompts"
SEARCH_PROMPT_PATH = PROMPTS_DIR / "search_prompt.md"



def load_prompt(path: Path) -> str:
    with path.open(encoding="utf-8") as prompt_file:
        return prompt_file.read()


provider = OpenAIProvider(api_key=settings.OPENAI_API_KEY)

model = OpenAIChatModel(model_name="gpt-5", provider=provider)

# Search Agent
search_agent = Agent(model=model, system_prompt=load_prompt(SEARCH_PROMPT_PATH))

