"""
carrega as variáveis de ambiente do arquivo .env.
falha rapido caso alguma variável de ambiente obrigatória não esteja presente.
"""
import os
from dotenv import load_dotenv
from dataclasses import dataclass

load_dotenv()

class ConfigError:
    """erro de configuração do ambiente"""
def _get_env(name : str) -> str:
    value = os.getenv(name)
    if value is None:
        raise ConfigError(f"variável de ambiente {name} não encontrada")
    return value

@dataclass(frozen=True)
class Settings:
    """configurações de ambiente"""
    supabase_url: str
    supabase_key: str
    zapi_instance_id: str
    zapi_token: str
    zapi_client_token: str
    max_contatos: 3

def load_settings() -> Settings:
    return Settings(
        supabase_url=_get_env("SUPABASE_URL"),
        supabase_key=_get_env("SUPABASE_KEY"),
        zapi_instance_id=_get_env("ZAPI_INSTANCE_ID"),
        zapi_token=_get_env("ZAPI_TOKEN"),
        zapi_client_token=_get_env("ZAPI_CLIENT_TOKEN"),
        max_contatos=int(os.getenv("MAX_CONTATOS", "3")),
    )