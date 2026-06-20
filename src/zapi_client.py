"""
cliente responsável por enviar mensagens via Z-API
"""
import logging
import requests
from src.config import Settings

logger = logging.getLogger(__name__)

class ZapiError(Exception):
    """erro ao enviar msg via Z-API"""

class ZapiClient:
    """envia msg via Z-API"""
    def __init__(self,settings: Settings):
        self.base_url = (
            f"https://api.z-api.io/instances/{settings.zapi_instance_id}"
            f"/token/{settings.zapi_token}/send-text"
        )

        self._headers = {
            "Content-Type": "application/json",
            "Client-Token": settings.zapi_client_token,
        }

    
    def enviar_mensagem(self, telefone: str, mensagem: str) -> None:
        payload = {"phone": telefone, "message": mensagem}

        try:
            response = requests.post (
                self._base_url, json=payload, headers=self._headers, timeout=15
            )
        except requests.RequestException as exc:
            raise ZapiError(f"erro ao enviar mensagem para {telefone}: {exc}") from exc

        if response.status_code >= 400:
           raise ZapiError(
                f"Z-API retornou erro {response.status_code} para {telefone}: {response.text}"
            )

        logger.info("Mensagem enviada com sucesso para %s.", telefone)