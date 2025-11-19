import pandas as pd
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def load_data():
    data_file = ROOT / "data" / "data.json"
    with open(data_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    obras = pd.DataFrame(data.get("obras", []))
    salas = pd.DataFrame(data.get("salas", []))
    entradas = pd.DataFrame(data.get("entradas", []))
    return obras, salas, entradas