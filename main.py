import os
import json
import time
import pandas as pd
from dotenv import load_dotenv
from rich.console import Console
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn

from modules.api_client import enviar_a_n8n

console = Console()
load_dotenv()

# ======================================================
# 🎭 BIENVENIDA LIMPIA Y PROFESIONAL
# ======================================================

def banner():
    os.system("cls" if os.name == "nt" else "clear")
    print("\n")
    print("╔══════════════════════════════════════════════════════╗")
    print("║        🎭  SISTEMA INTELIGENTE DE BOLETERÍA 2025     ║")
    print("║                Teatro Artech - Python + n8n          ║")
    print("╚══════════════════════════════════════════════════════╝\n")

def bienvenida():
    console.print("[bold cyan]Bienvenido al asistente inteligente del Teatro Artech.[/bold cyan]\n")
    console.print(
        "Podés realizar consultas sobre obras, funciones, salas, ventas, reportes "
        "y cualquier información disponible en el sistema.\n"
    )
    console.print("⚡ El sistema interpreta tu consulta, la envía a n8n y devuelve la respuesta automáticamente.")
    console.print("📄 Si la respuesta contiene datos tabulares, también se genera un archivo Excel.\n")
    console.print("[bold yellow]Escribí tu consulta abajo o ingresá 'salir' para finalizar.[/bold yellow]\n")


# ======================================================
# 📊 TABLAS + EXPORTACIÓN A EXCEL
# ======================================================

def imprimir_tabla(datos):
    if not datos:
        console.print("[bold red]No hay datos para mostrar[/bold red]")
        return

    table = Table(show_header=True, header_style="bold magenta")

    first = datos[0]
    for col in first.keys():
        table.add_column(col.capitalize())

    for row in datos:
        table.add_row(*[str(v) for v in row.values()])

    console.print(table)


def guardar_excel(datos):
    df = pd.DataFrame(datos)
    output_path = os.path.join(os.getcwd(), "Reporte.xlsx")
    df.to_excel(output_path, index=False)
    return output_path


# ======================================================
# 🔄 ANIMACIÓN “Procesando…”
# ======================================================

def esperar_respuesta():
    with Progress(
        SpinnerColumn(style="cyan"),
        TextColumn("[cyan]Procesando en n8n, por favor espere...[/cyan]"),
        transient=True
    ) as progress:
        progress.add_task("", total=None)
        time.sleep(1.2)


# ======================================================
# 📩 PROCESAR RESPUESTA DE N8N
# ======================================================

def procesar_respuesta(respuesta):
    console.print("\n[bold green]📩 Respuesta del sistema:[/bold green]\n")

    if isinstance(respuesta, dict) and "error" in respuesta:
        console.print(f"[bold red]❌ Error:[/bold red] {respuesta['error']}")
        return

    try:
        contenido = respuesta.get("resultado", respuesta)
        contenido = json.loads(contenido) if isinstance(contenido, str) else contenido
    except:
        contenido = respuesta

    # Texto simple
    if isinstance(contenido, str):
        console.print("[bold cyan]" + contenido.capitalize() + "[/bold cyan]")
        return 
    
    # Datos en tabla
    if isinstance(contenido, list):
        imprimir_tabla(contenido)
        try:
            console.print("\n[bold yellow]📁 Generando archivo Excel...[/bold yellow]")
            path = guardar_excel(contenido)
            console.print(f"[bold green]✔ Archivo guardado correctamente:[/bold green] {path}")
        except Exception as e:
            console.print("[bold red]❌ Error al generar Excel:[/bold red]", e)
        return
    
    console.print("[bold cyan]" + str(contenido).capitalize() + "[/bold cyan]")


# ======================================================
# 🚀 APLICACIÓN PRINCIPAL – CONSULTA LIBRE
# ======================================================

def main():
    while True:
        banner()
        bienvenida()

        consulta = input("💬 Escribí tu consulta: ").strip()

        if consulta.lower() in ("salir", "exit", "quit"):
            console.print("\n👋 [bold cyan]¡Saliendo del sistema inteligente![/bold cyan]")
            break

        if not consulta:
            console.print("[bold red]⚠ Ingresá una consulta válida.[/bold red]")
            time.sleep(1)
            continue

        esperar_respuesta()
        respuesta = enviar_a_n8n({"query": consulta})
        procesar_respuesta(respuesta)

        print("\n" + "-" * 60 + "\n")
        input("ENTER para realizar otra consulta...")


if __name__ == "__main__":
    main()
