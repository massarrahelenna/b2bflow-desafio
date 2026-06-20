"""
cliente responsavel por buscar contatos cadastrados no supabase
"""
import logging
from typing import List

from supabase import create_client, Client

from src.config import Settings
from src.models import Contato

logger = logging.getLogger(__name__)

class SupabaseContatoRepository:
    """repositório de contatos no supabase"""
    TABLE_NAME = "contatos"

    def __init__(self, settings: Settings):
        self.client: Client = create_client(settings.supabase_url, settings.supabase_key)

    def get_contatos(self, limite: int) -> List[Contato]:
        """retorna até o 'limite' contatos cadastrados no supabase (ordenados por data de criação)"""
        logger.info(f"Buscando até {limite} contato(s) no Supabase...")

        response = (
            self.client.table(self.TABLE_NAME)
            .select("nome, telefone")
            .order("created_at", desc=False)
            .limit(limite)
            .execute()
        )

        contatos = [Contato.from_dict(row) for row in response.data]
        logger.info(f"Encontrado(s) {len(contatos)} contato(s) no Supabase.")
        return contatos