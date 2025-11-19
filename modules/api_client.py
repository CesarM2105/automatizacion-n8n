"""# modules/api_client.py
import requests
from .config import N8N_URL, API_KEY

def enviar_a_n8n(query: str, timeout: int = 10):
    headers = {}
    if API_KEY:
        headers["Authorization"] = f"Bearer {API_KEY}"
    try:
        resp = requests.post(N8N_URL, json={"query": query}, headers=headers, timeout=timeout)
        resp.raise_for_status()
        return resp.json()
    except requests.RequestException as e:
        return {"error": str(e)}"""

# modules/api_client.py
import requests

# URL directa del webhook n8n
N8N_URL = "https://cesarm21.app.n8n.cloud/webhook/prod-api"

# Opcional: si NO usas autenticación, dejá esto vacío
USERNAME = "grupo2"
PASSWORD = "Pescar2025!"

def enviar_a_n8n(query: str, timeout: int = 600):
    try:
        resp = requests.post(
            N8N_URL,
            json={"query": query},
            auth=(USERNAME, PASSWORD) if USERNAME else None,  # ⬅️ Usa auth solo si hay user/pass
            timeout=timeout
        )
        resp.raise_for_status()
        return resp.json()
    except requests.RequestException as e:
        return {"error": str(e)}
