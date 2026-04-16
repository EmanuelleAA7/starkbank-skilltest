import os
import starkbank
from dotenv import load_dotenv

class ConfigError(Exception):
    """Exceção levantada para erros na configuração do SDK da Stark Bank."""
    pass

load_dotenv()

class Settings:
    PROJECT_ID = os.getenv("STARKBANK_PROJECT_ID")
    PRIVATE_KEY = os.getenv("STARKBANK_PRIVATE_KEY_CONTENT", "").replace('\\n', '\n')
    ENVIRONMENT = os.getenv("STARKBANK_ENVIRONMENT", "sandbox")

def init_starkbank():
    private_key = os.getenv("STARKBANK_PRIVATE_KEY_CONTENT")
    project_id = os.getenv("STARKBANK_PROJECT_ID")

    if not private_key or not project_id:
        raise ConfigError("Stark Bank credentials missing in environment variables.")

    try:
        starkbank.user = starkbank.Project(
            environment=os.getenv("STARKBANK_ENVIRONMENT", "sandbox"),
            id=project_id,
            private_key=private_key.replace('\\n', '\n')
        )
        print("SDK successfully authenticated.")
    except Exception as e:
        raise ConfigError(f"Failed to initialize Stark Project: {str(e)}")
