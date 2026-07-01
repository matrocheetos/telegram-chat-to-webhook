import os
from telethon.sync import TelegramClient

API_ID = int(os.getenv('API_ID', '0'))
API_HASH = os.getenv('API_HASH', '')

if API_ID == 0 or not API_HASH:
    print("ERRO: Defina as variáveis de ambiente API_ID e API_HASH antes de rodar.")
    exit(1)

os.makedirs('session', exist_ok=True)

print("Iniciando processo de autenticação do Telegram...")
temp_session = 'session/userbot_temp'
temp_session_file = 'session/userbot_temp.session'
final_session_file = 'session/userbot.session'

if os.path.exists(temp_session_file):
    try:
        os.remove(temp_session_file)
    except Exception:
        pass

try:
    with TelegramClient(temp_session, API_ID, API_HASH) as client:
        pass
    
    if os.path.exists(temp_session_file):
        if os.path.exists(final_session_file):
            try:
                os.remove(final_session_file)
            except Exception:
                pass
        os.rename(temp_session_file, final_session_file)
        print("\nSessão gerada e salva com sucesso em 'session/userbot.session'!")
        print("O container principal detectará o arquivo e iniciará o monitoramento em instantes.")
    else:
        print("\nErro: O arquivo temporário de sessão não foi encontrado.")
except Exception as e:
    print(f"\nFalha na autenticação: {e}")
    print("Dica: Se o erro for de número inválido, use o formato +55DDD999999999")
    print("Por favor, tente rodar o script novamente.")
