import os
import time
import requests
from telethon import TelegramClient, events

API_ID = int(os.getenv('API_ID', '0'))
API_HASH = os.getenv('API_HASH', '')
WEBHOOK_URL = os.getenv('WEBHOOK_URL', '')

AUTH_BASIC_USER = os.getenv('AUTH_BASIC_USER')
AUTH_BASIC_PASSWORD = os.getenv('AUTH_BASIC_PASSWORD')

AUTH_HEADER_NAME = os.getenv('AUTH_HEADER_NAME')
AUTH_HEADER_VALUE = os.getenv('AUTH_HEADER_VALUE')

AUTH_JWT_SECRET = os.getenv('AUTH_JWT_SECRET')
AUTH_JWT_ALGORITHM = os.getenv('AUTH_JWT_ALGORITHM', 'HS256')

cached_jwt_token = None
jwt_token_expires_at = 0

chats_env = os.getenv('MONITORED_CHATS', '@chat_1, @chat_2')
MONITORED_CHATS = [chat.strip() for chat in chats_env.split(',') if chat.strip()]

SESSION_FILE = 'session/userbot.session'

if not os.path.exists(SESSION_FILE):
    print("=========================================================")
    print("⚠️ AVISO: Nenhuma sessão do Telegram encontrada!")
    print("Para gerar a sessão, acesse o terminal do container e execute:")
    print("docker exec -it telegram-monitor python auth.py")
    print("Após gerar a sessão, este container iniciará o monitoramento automaticamente.")
    print("=========================================================")
    # Loop aguardando a criação do arquivo de sessão
    while not os.path.exists(SESSION_FILE):
        time.sleep(5)
    
    print("✅ Sessão detectada! Inicializando cliente...")

print("Iniciando monitor de promoções do Telegram...")
client = TelegramClient('session/userbot', API_ID, API_HASH)

@client.on(events.NewMessage(chats=MONITORED_CHATS))
async def handler(event):
    message_text = event.raw_text
    message_text_lower = message_text.lower()
    
    if WEBHOOK_URL:
        print(f"Mensagem recebida. Enviando para o webhook...")
        payload = {
            "text": message_text,
            "source": "telegram"
        }
        try:
            request_kwargs = {
                "json": payload,
                "timeout": 10
            }
            
            headers = {}
            if AUTH_BASIC_USER and AUTH_BASIC_PASSWORD:
                request_kwargs["auth"] = (AUTH_BASIC_USER, AUTH_BASIC_PASSWORD)
            elif AUTH_HEADER_NAME and AUTH_HEADER_VALUE:
                headers[AUTH_HEADER_NAME] = AUTH_HEADER_VALUE
            elif AUTH_JWT_SECRET:
                import jwt
                global cached_jwt_token, jwt_token_expires_at
                
                current_time = int(time.time())
                if not cached_jwt_token or current_time > (jwt_token_expires_at - 3600):
                    jwt_token_expires_at = current_time + 86400 # 24 horas
                    jwt_payload = {
                        "iss": "telegram-monitor",
                        "iat": current_time,
                        "exp": jwt_token_expires_at
                    }
                    cached_jwt_token = jwt.encode(jwt_payload, AUTH_JWT_SECRET, algorithm=AUTH_JWT_ALGORITHM)
                
                headers["Authorization"] = f"Bearer {cached_jwt_token}"
                
            if headers:
                request_kwargs["headers"] = headers

            requests.post(WEBHOOK_URL, **request_kwargs)
        except Exception as e:
            print(f"Erro ao enviar para o webhook: {e}")

def auth_failed():
    import sys
    print("=========================================================")
    print("⚠️ ERRO: A sessão atual do Telegram é inválida ou expirou!")
    print("Deletando o arquivo de sessão inválido automaticamente...")
    if os.path.exists(SESSION_FILE):
        try:
            os.remove(SESSION_FILE)
        except:
            pass
    print("Reiniciando o monitor...")
    print("=========================================================")
    os.execv(sys.executable, ['python'] + sys.argv)

client.start(phone=lambda: auth_failed())
client.run_until_disconnected()