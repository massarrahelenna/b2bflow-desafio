"""
ponto de entrada da aplicação:
lê os contatos cadastrados no supabase, e envia a msg "Olá {nome_contato}, tudo bem?" para cada contato via Z-API
"""
import logging
import sys

from src.config import ConfigError, load_settings
from src.messenger import Messenger
from src.supabase_client import SupabaseContatoRepository
from src.zapi_client import ZApiClient

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)

def main():
    try:
        settings = load_settings()
    except ConfigError as exc:
        logger.error("Erro de configuração: %s", exc)
        return 1

    repository = SupabaseContatoRepository(settings)
    zapi_client = ZApiClient(settings)
    messenger = Messenger(settings, repository, zapi_client)

    try:
        resultado = messenger.executar()
    except Exception:
        logger.exception("Erro inesperado durante a execução.")
        return 1

    if resultado["falhas"] > 0 and resultado["enviados"] == 0:
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())