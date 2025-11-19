# modules/chat.py
import re
# from difflib import get_close_matches
# from .report import ventas_por_mes

def clean_text(s: str) -> str:
    s = s.lower()
    s = re.sub(r"[^\w\s]", "", s)  # elimina signos de puntuación
    return s.strip()

# def find_title_for_actores(user: str, obras):
#     # intenta extraer "actores de <titulo>" o "actores <titulo>"
#     m = re.search(r"(?:actores|elenco)(?:\s+de)?\s+(.+)", user, re.I)
#     if not m:
#         return None
#     candidate = m.group(1).strip(" ?.!")
#     # fuzzy match con títulos existentes
#     if obras is None or obras.empty:
#         return candidate
#     titles = obras["titulo"].astype(str).tolist()
#     close = get_close_matches(candidate, titles, n=1, cutoff=0.6)
#     return close[0] if close else candidate

# def procesar_consulta(user: str, obras, entradas):
#     user_clean = clean_text(user)

#     # 1) Actores / elenco
#     title = find_title_for_actores(user, obras)
#     if title:
#         mask = obras["titulo"].str.lower() == title.lower()
#         if mask.any():
#             row = obras[mask].iloc[0]
#             elenco = row.get("elenco", [])
#             if isinstance(elenco, list):
#                 return f"El elenco de {row['titulo']} es: {', '.join(elenco)}"
#             return f"El elenco de {row['titulo']}: {elenco}"
#         return f"No encontré la obra '{title}'"

#     # 2) Ventas por mes (ej: "ventas octubre" o "ventas 10")
#     if "ventas" in user_clean:
#         # buscar nombre de mes o número
#         if "octubre" in user_clean:
#             return ventas_por_mes(entradas, 10).to_string(index=False)
#         m = re.search(r"ventas.*\b(\d{1,2})\b", user_clean)
#         if m:
#             mes = int(m.group(1))
#             return ventas_por_mes(entradas, mes).to_string(index=False)

    # Si no lo manejamos local, devolvemos None -> enviar a n8n
    #return None