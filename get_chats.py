import os
from telethon.sync import TelegramClient

API_ID = int(os.getenv('API_ID', '0'))
API_HASH = os.getenv('API_HASH', '')

if API_ID == 0 or not API_HASH:
    print("ERRO: Defina as variáveis de ambiente API_ID e API_HASH antes de executar.")
    exit(1)

print("Iniciando cliente para listar chats...")
with TelegramClient('session/homelab_userbot', API_ID, API_HASH) as client:
    print("\n--- SEUS GRUPOS E CANAIS ---")
    for dialog in client.iter_dialogs():
        if dialog.is_channel or dialog.is_group:
            identifier = f"@{dialog.entity.username}" if getattr(dialog.entity, 'username', None) else str(dialog.id)
            print(f"Nome: {dialog.name} | Identificador: {identifier}")
    print("----------------------------\n")
    print("Copie os valores da coluna 'Identificador' e cole na sua variável MONITORED_CHATS.")
