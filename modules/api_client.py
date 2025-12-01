# modules/api_client.py
import requests

# URL directa del webhook n8n
N8N_URL = "https://cesarm21.app.n8n.cloud/webhook/prod-api"

# Autenticación básica (coincide con tu n8n)
USERNAME = "grupo2"
PASSWORD = "Pescar2025!"

def enviar_a_n8n(payload, timeout: int = 600):
    try:
        resp = requests.post(
            N8N_URL,
            json=payload,
            auth=(USERNAME, PASSWORD),
            timeout=timeout
        )
        resp.raise_for_status()
        return resp.json()
    except requests.RequestException as e:
        return {"error": str(e)}
