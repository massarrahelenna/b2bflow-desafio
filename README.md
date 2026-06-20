# b2bflow - Desafio Estágio Python

Script que lê contatos cadastrados no Supabase e envia, via Z-API, a mensagem
personalizada:

> Olá, `<nome_contato>` tudo bem com você?

para até 3 contatos diferentes.

## Setup da tabela no Supabase

No SQL Editor do seu projeto Supabase, rode:

```sql
create table contatos (
  id bigint generated always as identity primary key,
  nome text not null,
  telefone text not null,
  created_at timestamp default now()
);

insert into contatos (nome, telefone) values
('João', '5599999999999'),
('Maria', '5599888888888'),
('Pedro', '5599777777777');
```

> O telefone deve estar no formato `55DDDNUMERO` (DDI + DDD + número, sem
> espaços, sem `+`), conforme exigido pela Z-API.

Pegue em **Project Settings > API Keys**:
- `Project URL` (https://SEU_PROJECT_ID.supabase.co) → `SUPABASE_URL`
- `secret key` → `SUPABASE_KEY`

## Variáveis de ambiente (.env)

Copie o arquivo de exemplo e preencha com seus dados:

```bash
cp .env.example .env
```

```env
SUPABASE_URL=https://SEU_PROJETO.supabase.co
SUPABASE_KEY=SUA_SECRET_KEY

ZAPI_INSTANCE_ID=SEU_INSTANCE_ID
ZAPI_TOKEN=SEU_TOKEN
ZAPI_CLIENT_TOKEN=SEU_CLIENT_TOKEN_SECURITY

MAX_CONTATOS=3
```

As credenciais da Z-API (`ZAPI_INSTANCE_ID`, `ZAPI_TOKEN` e `ZAPI_CLIENT_TOKEN`)
ficam no painel da sua instância em [z-api.io](https://www.z-api.io), na aba
"Dados da instância web" (Instance ID e Token) e na aba "Segurança"
(Client-Token).

## Como rodar

```bash
# instalar dependências
pip install -r requirements.txt

# rodar o script
python3 main.py
```

## Como rodar os testes

```bash
pytest
```

## Evidências de funcionamento

### Execução do script

```
$ python3 main.py
2026-06-20 20:02:29 [INFO] src.supabase_client: Buscando até 3 contato(s) no Supabase...
2026-06-20 20:02:30 [INFO] src.supabase_client: Encontrado(s) 3 contato(s) no Supabase.
2026-06-20 20:02:30 [INFO] src.zapi_client: Mensagem enviada com sucesso para 556199568432.
2026-06-20 20:02:30 [INFO] src.zapi_client: Mensagem enviada com sucesso para 5512997079111.
2026-06-20 20:02:30 [INFO] src.zapi_client: Mensagem enviada com sucesso para 5561991686474.
2026-06-20 20:02:30 [INFO] src.messenger: Concluído. Enviados: 3 | Falhas: 0
```

### Mensagens recebidas no WhatsApp

![Mensagem recebida](./docs/evidencia-whatsapp.png)

> Observação: por se tratar de uma conta **Z-API em plano trial**, cada
> mensagem enviada vem acompanhada automaticamente de um aviso padrão da
> própria Z-API ("MENSAGEM DE TESTE — Esta mensagem foi enviada por uma
> CONTA EM TRIAL"). Esse aviso é um comportamento da plataforma no plano
> gratuito, não faz parte do código. A mensagem real enviada pela aplicação
> é a que aparece destacada após "Corpo da mensagem enviada" no print.

## Autor

**Helenna Massarra Paes**
Desafio técnico — Estágio em Desenvolvimento Python (b2bflow)
[GitHub](https://github.com/massarrahelenna)
