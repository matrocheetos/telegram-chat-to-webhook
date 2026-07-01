# Testando a Integração com Webhook

Este repositório fornece o script auxiliar [send_test.py](send_test.py) para simular o envio de mensagens do Telegram para a URL de webhook configurada. Ele replica exatamente o mesmo formato de payload e o mesmo fluxo de autenticação (JWT, Basic Auth ou headers customizados) usados pelo [monitor.py](monitor.py).

## Como Executar

### 1. Dentro do Container Docker (Recomendado)

O script já vem embutido na imagem do container e lê automaticamente as variáveis de ambiente configuradas no seu `compose.yaml`.

Para enviar uma mensagem de teste padrão ("Esta é uma mensagem de teste do Telegram"):
```bash
docker exec telegram-monitor python send_test.py
```

Para enviar uma mensagem de teste com um texto personalizado:
```bash
docker exec telegram-monitor python send_test.py --text "Olá! Esta é uma mensagem personalizada"
```

Para simular o envio a partir de um chat ID específico do Telegram (por padrão envia `123456789`):
```bash
docker exec telegram-monitor python send_test.py --source "-1002479272437"
```

---

### 2. Fora do Container Docker (Localmente)

Se você preferir executar o script localmente no seu computador, certifique-se de instalar as dependências necessárias primeiro:

```bash
pip install -r requirements.txt
```

E em seguida, execute o script passando a URL e as credenciais via argumentos de linha de comando:

```bash
python send_test.py --url "https://n8n.seuservidor.com/webhook-test/seu-uuid" --text "Teste local"
```

---

## Opções de Linha de Comando

O script suporta os seguintes parâmetros para personalização:

| Parâmetro | Descrição | Padrão |
|---|---|---|
| `--url` / `-u` | A URL do webhook de destino. | Valor da variável de ambiente `WEBHOOK_URL` |
| `--text` / `-t` | O texto da mensagem a ser enviada. | `"Esta é uma mensagem de teste do Telegram"` |
| `--source` / `-s`| O ID de origem da mensagem (ID do grupo/canal). | `"123456789"` |
| `--jwt-secret` | A chave secreta para assinar o token JWT. | Valor da variável de ambiente `AUTH_JWT_SECRET` |
| `--jwt-alg` | O algoritmo de assinatura JWT. | Valor de `AUTH_JWT_ALGORITHM` ou `"HS256"` |
| `--basic-user` | Nome de usuário para autenticação básica HTTP. | Valor de `AUTH_BASIC_USER` |
| `--basic-pass` | Senha para autenticação básica HTTP. | Valor de `AUTH_BASIC_PASSWORD` |
| `--header-name` | Nome de um header HTTP customizado. | Valor de `AUTH_HEADER_NAME` |
| `--header-value`| Valor do header HTTP customizado. | Valor de `AUTH_HEADER_VALUE` |

---

## Formato do Payload Enviado

A requisição enviada ao Webhook é do tipo `POST` com `Content-Type: application/json` e o seguinte formato no corpo (`body`):

```json
{
  "text": "Esta é uma mensagem de teste do Telegram",
  "source": "123456789"
}
```
