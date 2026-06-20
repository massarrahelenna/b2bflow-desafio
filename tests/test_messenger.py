"""Testes unitários simples usando mocks (não requerem conexão real)."""
from unittest.mock import MagicMock

from src.config import Settings
from src.messenger import Messenger
from src.models import Contato


def _settings() -> Settings:
    return Settings(
        supabase_url="https://fake.supabase.co",
        supabase_key="fake-key",
        zapi_instance_id="fake-instance",
        zapi_token="fake-token",
        zapi_client_token="fake-client-token",
        max_contatos=3,
    )


def test_montar_mensagem_personaliza_nome():
    contato = Contato(nome="Maria", telefone="5599999999999")
    mensagem = Messenger.montar_mensagem(contato)
    assert mensagem == "Olá, Maria tudo bem com você?"


def test_executar_envia_para_todos_os_contatos():
    contatos = [
        Contato(nome="João", telefone="5599999999999"),
        Contato(nome="Maria", telefone="5599888888888"),
    ]

    repository = MagicMock()
    repository.listar_contatos.return_value = contatos

    zapi_client = MagicMock()

    messenger = Messenger(_settings(), repository, zapi_client)
    resultado = messenger.executar()

    assert resultado == {"enviados": 2, "falhas": 0}
    assert zapi_client.enviar_mensagem.call_count == 2


def test_executar_sem_contatos_nao_envia_nada():
    repository = MagicMock()
    repository.listar_contatos.return_value = []

    zapi_client = MagicMock()

    messenger = Messenger(_settings(), repository, zapi_client)
    resultado = messenger.executar()

    assert resultado == {"enviados": 0, "falhas": 0}
    zapi_client.enviar_mensagem.assert_not_called()