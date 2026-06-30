import os
import requests
from telethon import TelegramClient, events

API_ID = int(os.getenv('API_ID', '0'))
API_HASH = os.getenv('API_HASH', '')
WEBHOOK_URL = os.getenv('WEBHOOK_URL', '')

chats_env = os.getenv('MONITORED_CHATS', '@chat_1, @chat_2')
MONITORED_CHATS = [chat.strip() for chat in chats_env.split(',') if chat.strip()]

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
            requests.post(WEBHOOK_URL, json=payload, timeout=10)
        except Exception as e:
            print(f"Erro ao enviar para o webhook: {e}")

client.start()
client.run_until_disconnected()