import os
from telethon.sync import TelegramClient

API_ID = int(os.getenv('API_ID', '0'))
API_HASH = os.getenv('API_HASH', '')

if API_ID == 0 or not API_HASH:
    print("ERRO: Defina as variáveis de ambiente API_ID e API_HASH antes de rodar.")
    exit(1)

print("Iniciando processo de autenticação do Telegram...")
# O Telethon vai pedir o número de telefone e código do SMS interativamente
with TelegramClient('session/userbot', API_ID, API_HASH) as client:
    print("\n✅ Sessão gerada e salva com sucesso em 'session/userbot.session'!")
    print("O container principal detectará o arquivo e iniciará o monitoramento em instantes.")
