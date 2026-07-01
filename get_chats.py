import os
import shutil
import glob
from telethon.sync import TelegramClient

API_ID = int(os.getenv('API_ID', '0'))
API_HASH = os.getenv('API_HASH', '')

if API_ID == 0 or not API_HASH:
    print("ERRO: Defina as variáveis de ambiente API_ID e API_HASH antes de executar.")
    exit(1)

SESSION_FILE = 'session/userbot.session'
TEMP_PREFIX = 'session/userbot_get_chats_temp'
TEMP_COPY = f'{TEMP_PREFIX}.session'

if not os.path.exists(SESSION_FILE):
    print("ERRO: O arquivo de sessão 'session/userbot.session' não foi encontrado.")
    print("Por favor, execute o script de autenticação primeiro:")
    print("docker exec -it telegram-monitor python auth.py")
    exit(1)

shutil.copyfile(SESSION_FILE, TEMP_COPY)

try:
    print("Iniciando cliente para listar chats...")
    with TelegramClient(TEMP_PREFIX, API_ID, API_HASH) as client:
        chats = []
        for dialog in client.iter_dialogs():
            if dialog.is_channel or dialog.is_group:
                identifier = f"@{dialog.entity.username}" if getattr(dialog.entity, 'username', None) else str(dialog.id)
                name = dialog.name or ""
                if len(name) > 100:
                    name = name[:97] + "..."
                chats.append((identifier, name))

        header_id = "ID"
        header_name = "Nome"
        max_id_len = max((len(c[0]) for c in chats), default=15)
        max_id_len = max(max_id_len, len(header_id))

        print(f"{header_id.ljust(max_id_len)} | {header_name}")
        print(f"{'-' * max_id_len}-+-{'-' * 40}")
        for identifier, name in chats:
            print(f"{identifier.ljust(max_id_len)} | {name}")
        print(f"{'-' * max_id_len}-+-{'-' * 40}\n")
        print("Copie os valores da coluna 'ID' e cole na sua variável MONITORED_CHATS.")
finally:
    for f in glob.glob(f"{TEMP_PREFIX}.session*"):
        try:
            os.remove(f)
        except Exception:
            pass
