# load_env.py
from pathlib import Path
from dotenv import load_dotenv

def load_env():
    """Force-load .env from the agent_demo directory."""
    env_path = Path(__file__).parent / ".env"
    load_dotenv(dotenv_path=env_path)
