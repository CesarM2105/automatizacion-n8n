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
# 🎭 BIENVENIDA
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
        "Podés consultar obras, funciones, salas, ventas o generar reportes automáticos.\n"
        "El sistema procesa tu consulta, usa IA + SQL + n8n y devuelve resultados.\n"
    )
    console.print("📄 Si los datos son tabulares, se genera un archivo Excel.\n")
    console.print("[bold yellow]Escribí tu consulta o 'salir' para finalizar.[/bold yellow]\n")


# ======================================================
# 📊 TABLAS + EXCEL
# ======================================================

def imprimir_tabla(datos):
    if not datos:
        console.print("[bold red]No hay datos para mostrar[/bold red]")
        return

    table = Table(show_header=True, header_style="bold magenta")
    for col in datos[0].keys():
        table.add_column(col.capitalize())

    for row in datos:
        table.add_row(*[str(v) for v in row.values()])

    console.print(table)


def guardar_excel(datos, name="Reporte.xlsx"):
    df = pd.DataFrame(datos)
    output_path = os.path.join(os.getcwd(), name)
    df.to_excel(output_path, index=False)
    return output_path


# ======================================================
# 🔄 ANIMACIÓN
# ======================================================

def esperar_respuesta():
    with Progress(
        SpinnerColumn(style="cyan"),
        TextColumn("[cyan]Procesando en n8n...[/cyan]"),
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

    # ============================
    # Si viene texto simple
    # ============================
    if isinstance(contenido, str):
        console.print("[bold cyan]" + contenido.capitalize() + "[/bold cyan]")
        return
    
    # ============================
    # Si es tabla (datos en lista)
    # ============================
    if isinstance(contenido, list):

        # 1️⃣ Mostrar tabla
        console.print("🗂 [bold cyan]Datos generados:[/bold cyan]\n")
        imprimir_tabla(contenido)

        # 2️⃣ Crear Excel por defecto
        try:
            path = guardar_excel(contenido)
            console.print(f"\n[bold green]✔ Archivo Excel creado:[/bold green] {path}")
        except Exception as e:
            console.print(f"[bold red]❌ Error al generar Excel:[/bold red] {e}")

        # 3️⃣ Si la consulta incluye “enviar mail” → Excel especial
        if "mail" in respuesta.get("accion", "").lower() or \
           "correo" in respuesta.get("accion", "").lower() or \
           "gmail" in respuesta.get("accion", "").lower():

            console.print("\n📨 [bold yellow]Preparando archivo para enviar por correo...[/bold yellow]\n")

            try:
                path_email = guardar_excel(contenido, "Reporte_Email.xlsx")
                console.print(f"[bold green]📁 Archivo creado para envío por correo:[/bold green] {path_email}")
                console.print("[bold cyan]📤 El correo fue enviado correctamente.[/bold cyan]")
            except Exception as e:
                console.print(f"[bold red]❌ Error al crear archivo para email:[/bold red] {e}")

        return
    
    # Si no encaja en nada:
    console.print("[bold cyan]" + str(contenido).capitalize() + "[/bold cyan]")


# ======================================================
# 🚀 PROGRAMA PRINCIPAL
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
        input("ENTER para seguir...")


if __name__ == "__main__":
    main()
