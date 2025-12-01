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
# 🎭 ESTILO VISUAL DE LA CONSOLA
# ======================================================

def banner():
    os.system("cls" if os.name == "nt" else "clear")
    print("\n")
    print("╔══════════════════════════════════════════════════════╗")
    print("║        🎭  SISTEMA INTELIGENTE DE BOLETERÍA 2025     ║")
    print("║                Teatro Artech - Python + n8n          ║")
    print("╚══════════════════════════════════════════════════════╝\n")


def mostrar_menu():
    console.print("📌 [bold cyan]Opciones disponibles:[/bold cyan]\n")
    print("1️⃣  Consulta general (IA + SQL + n8n)")
    print("2️⃣  Ejemplos de consultas")
    print("3️⃣  Salir\n")


def ejemplos():
    console.print("\n📘 [bold cyan]EJEMPLOS DE CONSULTAS[/bold cyan]\n")
    print("🎭 Obras:")
    print("   • ¿Quiénes son los actores de Hamlet?")
    print("   • ¿Qué obras hay esta semana?")
    print("   • Mostrame la descripción de la obra El Rey León.\n")
    
    print("💺 Salas y Ubicaciones:")
    print("   • ¿Qué capacidad tiene la sala principal?")
    print("   • Mostrame las ubicaciones de la sala Roja.\n")
    
    print("🎟 Entradas:")
    print("   • ¿Cuántas entradas se vendieron en octubre?")
    print("   • ¿Cuáles fueron las ventas por medio de pago?\n")

    print("📄 Reportes:")
    print("   • Generar Excel con la cartelera del mes.")
    print("   • Enviar por mail listado de compras de un cliente.\n")

    print("💡 Todo lo procesa n8n con SQL + API + IA.\n")

# ======================================================
# 🔥 FORMATO TABLA + EXCEL
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
# 🔥 ANIMACIÓN “CARGANDO…”
# ======================================================

def esperar_respuesta():
    with Progress(
        SpinnerColumn(style="cyan"),
        TextColumn("[cyan]Procesando en n8n, por favor espere...[/cyan]"),
        transient=True
    ) as progress:
        progress.add_task("", total=None)
        time.sleep(1.5)


# ======================================================
# 🚀 PROCESAR RESPUESTA DEL WEBHOOK N8N
# ======================================================

def procesar_respuesta(respuesta):
    console.print("\n[bold green]📩 Respuesta del sistema:[/bold green]\n")

    # Error de conexión
    if isinstance(respuesta, dict) and "error" in respuesta:
        console.print(f"[bold red]❌ Error:[/bold red] {respuesta['error']}")
        return

    try:
        contenido = respuesta.get("resultado", respuesta)
        contenido = json.loads(contenido) if isinstance(contenido, str) else contenido
    except:
        contenido = respuesta

    # Si es texto simple
    if isinstance(contenido, str):
        console.print("[bold cyan]" + contenido.capitalize() + "[/bold cyan]")
        return 
    
    # Si es tabla
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
# 🎮 APLICACIÓN PRINCIPAL
# ======================================================

def main():
    while True:
        banner()
        mostrar_menu()

        opcion = input("👉 Seleccioná una opción (1-3): ").strip()

        if opcion == "3":
            console.print("\n👋 [bold cyan]¡Saliendo del sistema inteligente![/bold cyan]")
            break

        if opcion == "2":
            banner()
            ejemplos()
            input("\nENTER para volver al menú...")
            continue

        if opcion == "1":
            consulta = input("\n💬 Escribí tu consulta: ").strip()

            if not consulta:
                console.print("[bold red]⚠ Escribí una consulta válida.[/bold red]")
                input("\nENTER para continuar...")
                continue

            esperar_respuesta()
            respuesta = enviar_a_n8n({"query": consulta})
            procesar_respuesta(respuesta)

            print("\n" + "-"*60 + "\n")
            input("ENTER para continuar...")
            continue

        console.print("[bold red]⚠ Opción inválida[/bold red]")
        input("\nENTER para continuar...")

if __name__ == "__main__":
    main()
