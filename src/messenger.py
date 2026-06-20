"""
orquestra o fluxo: busca cliente -> monta msg -> envia msg via Z-API
"""
import logging
from typing import List

from src.config import Settings
from src.models import Contato
from src.supabase_client import SupabaseContatoRepository
from src.zapi_client import ZApiClient, ZApiError

logger = logging.getLogger(__name__)

MENSAGEM_TEMPLATE = "Oii {nome_contato}, tudo bem?"

class Mensager:
    def __init__(
            self,
            settings: Settings,
            repository: SupabaseContatoRepository,
            zapi_client: ZApiClient,
    ):
        self._settings = settings
        self._repository = repository
        self._zapi_client = zapi_client

    @staticmethod
    def montar_mensagem(contato: Contato) -> str:
        return MENSAGEM_TEMPLATE.format(nome_contato=contato.nome)
    
    def executar(self) -> dict:
        """Executa o fluxo completo e retorna um resumo do resultado (sucesso ou falha)"""
        contatos: List[Contato] = self._repository.listar_contatos(
            limite=self._setting.max_contatos
        )

        if not contatos:
            logger.warning("nenhum contato encontrado no supabase")
            return {"enviados": 0, "falhas": 0 }
        
        enviados = 0
        falhas = 0

        for contato in contatos:
            mensagem = self.montar_mensagem(contato)
            try:
                self._zapi_client.enviar_mensagem(contato.telefone, mensagem)
                enviados += 1
            except ZApiError as exc:
                logger.error("Erro ao enviar mensagem para %s: %s", contato.nome, exc)
                falhas += 1

        logger.info("Concluído. Enviados: %d | Falhas: %d", enviados, falhas)
        return {"enviados": enviados, "falhas": falhas}