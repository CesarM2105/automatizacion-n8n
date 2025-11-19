# modules/report.py
import pandas as pd

def ventas_por_mes(entradas, mes):
    df = entradas.copy()
    df["fecha_compra"] = pd.to_datetime(df["fecha_compra"], errors="coerce")
    filtrado = df[df["fecha_compra"].dt.month == mes]
    return filtrado[["codigo", "cliente", "fecha_compra"]]
