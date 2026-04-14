import starkbank
from dotenv import load_dotenv
import os

load_dotenv()

def init_starkbank():
    """Inicializa o SDK do Stark Bank com as credenciais do .env"""
    private_key = os.getenv("STARKBANK_PRIVATE_KEY_CONTENT")
    project_id = os.getenv("STARKBANK_PROJECT_ID")
    environment = os.getenv("STARKBANK_ENVIRONMENT", "sandbox")

    if not private_key or not project_id:
        raise ValueError("Credenciais do Stark Bank não configuradas no .env")

    starkbank.user = starkbank.Project(
        environment=environment,
        id=project_id,
        private_key=private_key,
    )