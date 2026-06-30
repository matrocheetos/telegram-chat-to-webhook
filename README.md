# Telegram Chat to Webhook

Este projeto é um bot (userbot) do Telegram construído em Python usando a biblioteca Telethon. Sua única função é monitorar mensagens recebidas em canais ou grupos específicos e encaminhá-las automaticamente para um Webhook HTTP externo, permitindo que você crie automações avançadas (como alertas de preços, extração de cupons, etc.) baseadas em mensagens do Telegram.

## Como Funciona

1. O script se autentica na rede do Telegram usando a sua conta de usuário (Userbot).
2. Ele fica "escutando" em tempo real os canais/grupos que você definiu nas variáveis de ambiente.
3. Quando uma nova mensagem chega nesses grupos, o script empacota o texto bruto da mensagem e o ID do chat em um formato JSON.
4. O payload JSON é enviado via `POST` para a URL do Webhook que você configurou.

## Variáveis de Ambiente

O comportamento do container é inteiramente controlado por variáveis de ambiente. Abaixo estão todas as variáveis disponíveis:

| Variável | Valor Padrão | Função |
|----------|--------------|--------|
| `API_ID` | `0` | ID da API do Telegram |
| `API_HASH` | `(vazio)` | Hash da API do Telegram |
| `WEBHOOK_URL` | `(vazio)` | A URL completa para onde o JSON da mensagem será enviado via método POST (ex: `http://n8n:5678/webhook/telegram`). |
| `MONITORED_CHATS` | `@canal_1, @canal_2` | Uma lista separada por vírgula contendo os `@usernames` públicos ou os `IDs` numéricos (ex: `-1001234567`) dos canais/grupos que o bot deve monitorar. |

## Como obter as Credenciais e IDs

### 1. Obtendo `API_ID` e `API_HASH`
Para conectar no Telegram com seu próprio usuário, você precisa registrar um app de desenvolvimento:
1. Acesse [my.telegram.org](https://my.telegram.org/) e faça login com seu número.
2. Vá em **API development tools**.
3. Crie um aplicativo preenchendo os dados (pode ser qualquer nome).
4. Copie o **App api_id** e o **App api_hash**.

### 2. Obtendo o ID numérico ou Username dos Chats
Se o grupo for privado, ele não possui um `@username`, então você precisa do ID numérico dele. Para facilitar isso, este repositório possui o script auxiliar `get_chats.py`.

Rode o comando abaixo após iniciar o container para listar todos os grupos em que você está e copiar seus respectivos IDs numéricos ou `@usernames`:
```bash
docker exec -it telegram-monitor python get_chats.py
```

## Docker Compose

Exemplo de configuração para o `compose.yaml`:

```yaml
services:
    telegram-monitor:
        image: ghcr.io/matrocheetos/telegram-monitor:latest
        container_name: telegram-monitor
        restart: unless-stopped
        volumes:
            - ./telegram-session:/app/session
        environment:
            - API_ID=12345678
            - API_HASH=abcdef1234567890abcdef
            - WEBHOOK_URL=http://n8n:5678/webhook/telegram
            - MONITORED_CHATS=@canal_1, -100987654321
```

> **Atenção no Primeiro Uso:** Na primeira vez que o container subir, o Telethon precisará autenticar sua sessão. Você precisará olhar os logs do container (`docker logs -f telegram-monitor`) ou anexar ao terminal interativo (`docker attach telegram-monitor`) para inserir o seu número de telefone e o código recebido por SMS no aplicativo do Telegram. Após isso, um arquivo `.session` será salvo no volume mapeado.
