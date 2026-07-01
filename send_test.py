import os
import sys
import time
import argparse
import requests
import jwt

def main():
    parser = argparse.ArgumentParser(
        description="Envia uma requisição de teste para o webhook no mesmo formato que o monitor.py."
    )
    parser.add_argument(
        "--url", "-u",
        default=os.getenv("WEBHOOK_URL"),
        help="URL do Webhook (Padrão: valor de WEBHOOK_URL do ambiente)"
    )
    parser.add_argument(
        "--text", "-t",
        default="Esta é uma mensagem de teste do Telegram",
        help="Texto da mensagem de teste"
    )
    parser.add_argument(
        "--jwt-secret",
        default=os.getenv("AUTH_JWT_SECRET"),
        help="Segredo JWT (Padrão: valor de AUTH_JWT_SECRET do ambiente)"
    )
    parser.add_argument(
        "--jwt-alg",
        default=os.getenv("AUTH_JWT_ALGORITHM", "HS256"),
        help="Algoritmo JWT (Padrão: valor de AUTH_JWT_ALGORITHM ou HS256)"
    )
    parser.add_argument(
        "--basic-user",
        default=os.getenv("AUTH_BASIC_USER"),
        help="Usuário para Basic Auth (Padrão: valor de AUTH_BASIC_USER)"
    )
    parser.add_argument(
        "--basic-pass",
        default=os.getenv("AUTH_BASIC_PASSWORD"),
        help="Senha para Basic Auth (Padrão: valor de AUTH_BASIC_PASSWORD)"
    )
    parser.add_argument(
        "--header-name",
        default=os.getenv("AUTH_HEADER_NAME"),
        help="Nome do Header Customizado (Padrão: valor de AUTH_HEADER_NAME)"
    )
    parser.add_argument(
        "--header-value",
        default=os.getenv("AUTH_HEADER_VALUE"),
        help="Valor do Header Customizado (Padrão: valor de AUTH_HEADER_VALUE)"
    )
    parser.add_argument(
        "--source", "-s",
        default="123456789",
        help="ID de origem da mensagem (Padrão: '123456789')"
    )

    args = parser.parse_args()

    if not args.url:
        print("ERRO: URL do webhook não definida. Defina a variável de ambiente WEBHOOK_URL ou use a opção --url / -u.")
        sys.exit(1)

    payload = {
        "text": args.text,
        "source": args.source
    }

    request_kwargs = {
        "json": payload,
        "timeout": 10
    }

    headers = {}

    if args.basic_user and args.basic_pass:
        print(f"-> Usando autenticação Basic Auth com usuário '{args.basic_user}'")
        request_kwargs["auth"] = (args.basic_user, args.basic_pass)
    elif args.header_name and args.header_value:
        print(f"-> Usando header customizado: {args.header_name}")
        headers[args.header_name] = args.header_value
    elif args.jwt_secret:
        print("-> Gerando token JWT para autenticação...")
        current_time = int(time.time())
        jwt_payload = {
            "iss": "telegram-monitor",
            "iat": current_time,
            "exp": current_time + 86400  # 24 horas
        }
        token = jwt.encode(jwt_payload, args.jwt_secret, algorithm=args.jwt_alg)
        headers["Authorization"] = f"Bearer {token}"

    if headers:
        request_kwargs["headers"] = headers

    print(f"\nEnviando requisição POST para: {args.url}")
    print(f"Payload: {payload}")
    if headers:
        logged_headers = headers.copy()
        if "Authorization" in logged_headers:
            logged_headers["Authorization"] = logged_headers["Authorization"][:20] + "..."
        print(f"Headers: {logged_headers}")

    try:
        response = requests.post(args.url, **request_kwargs)
        print(f"\n[Resposta do Servidor]")
        print(f"Status Code: {response.status_code}")
        print(f"Conteúdo: {response.text}")
    except Exception as e:
        print(f"\nERRO ao conectar com o webhook: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
