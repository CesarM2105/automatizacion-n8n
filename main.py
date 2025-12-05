
import os
import json
import time
import pandas as pd
import platform
from dotenv import load_dotenv
from rich.console import Console
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn

from modules.api_client import enviar_a_n8n

console = Console()
load_dotenv()

# ======================================================
# 📂 CONFIGURACIÓN DE RUTAS DE DESCARGA
# ======================================================

def obtener_ruta_descargas():
    """Retorna la ruta raíz del usuario (Desktop o Descargas según SO)"""
    home = os.path.expanduser("~")
    
    if platform.system() == "Windows":
        desktop = os.path.join(home, "Desktop")
        return desktop if os.path.exists(desktop) else home
    else:
        desktop = os.path.join(home, "Desktop")
        descargas = os.path.join(home, "Descargas")
        if os.path.exists(desktop):
            return desktop
        if os.path.exists(descargas):
            return descargas
        return home


# ======================================================
# 🎭 BIENVENIDA LIMPIA
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
        "Podés realizar consultas sobre obras, funciones, salas, ventas y reportes.\n"
        "El sistema interpreta tu consulta, la envía a n8n y devuelve la respuesta automáticamente.\n"
    )
    console.print("📄 Si la respuesta contiene datos tabulares, se genera un archivo Excel y CSV.\n")
    console.print("[bold yellow]Escribí tu consulta abajo o ingresá 'salir'.[/bold yellow]\n")


# ======================================================
# 📊 TABLAS + EXPORTACIÓN A EXCEL
# ======================================================

def imprimir_tabla(datos):
    if not datos:
        console.print("[bold red]No hay datos para mostrar.[/bold red]")
        return

    table = Table(show_header=True, header_style="bold magenta")

    for col in datos[0].keys():
        table.add_column(col.capitalize())

    for row in datos:
        table.add_row(*[str(v) for v in row.values()])

    console.print(table)


def guardar_excel(datos, nombre="Reporte"):
    """Guarda archivo Excel y notifica al usuario."""
    try:
        df = pd.DataFrame(datos)
        descargas = obtener_ruta_descargas()
        path = os.path.join(descargas, f"{nombre}_{int(time.time())}.xlsx")
        df.to_excel(path, index=False)

        console.print(f"\n[bold green]✔ Archivo Excel generado correctamente[/bold green]")
        console.print(f"[yellow]📁 Ubicación:[/yellow] [cyan]{path}[/cyan]\n")
        return path

    except Exception as e:
        console.print(f"[bold red]❌ Error al guardar Excel:[/bold red] {e}")
        return None


def guardar_csv(datos, nombre="Reporte"):
    """Guarda archivo CSV y notifica al usuario."""
    try:
        df = pd.DataFrame(datos)
        descargas = obtener_ruta_descargas()
        path = os.path.join(descargas, f"{nombre}_{int(time.time())}.csv")
        df.to_csv(path, index=False)

        console.print(f"[bold green]✔ Archivo CSV generado correctamente[/bold green]")
        console.print(f"[yellow]📁 Ubicación:[/yellow] [cyan]{path}[/cyan]\n")
        return path

    except Exception as e:
        console.print(f"[bold red]❌ Error al guardar CSV:[/bold red] {e}")
        return None


# ======================================================
# 🔍 DETECTOR DE TIPO DE RESPUESTA
# ======================================================

def detectar_tipo_respuesta(contenido):
    """Detecta si la respuesta es email, tabla o genérica."""
    if isinstance(contenido, dict):
        claves = [k.lower() for k in contenido.keys()]
        if any(x in claves for x in ["email", "correo", "mensaje", "asunto"]):
            return "email"
        if "output" in claves:
            return "email_output"

    if isinstance(contenido, list) and len(contenido) > 0:
        if isinstance(contenido[0], dict):
            claves = [k.lower() for k in contenido[0].keys()]
            if any(x in claves for x in ["email", "correo", "nombre"]):
                return "email"
        return "tabla"

    return "texto"


# ======================================================
# 🔄 ANIMACIÓN “Procesando…”
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
# 📩 PROCESAR RESPUESTA (LIMPIO, PROFESIONAL, ORDENADO)
# ======================================================

def procesar_respuesta(respuesta):
    console.print("\n[bold green]📩 Respuesta del sistema:[/bold green]\n")

    if isinstance(respuesta, dict) and "error" in respuesta:
        console.print(f"[bold red]❌ Error:[/bold red] {respuesta['error']}")
        return

    try:
        contenido = respuesta.get("resultado", respuesta)
        if isinstance(contenido, str):
            contenido = json.loads(contenido)
    except:
        contenido = respuesta

    tipo = detectar_tipo_respuesta(contenido)

    # 👉 1) Texto simple
    if tipo == "texto":
        console.print(f"[cyan]{str(contenido)}[/cyan]\n")
        return

    # 👉 2) Email simple
    if tipo == "email" and isinstance(contenido, dict):
        console.print("[bold cyan]📧 Datos del correo:[/bold cyan]")
        tabla = Table(show_header=True, header_style="bold cyan")
        tabla.add_column("Campo")
        tabla.add_column("Valor")

        for k, v in contenido.items():
            tabla.add_row(k.upper(), str(v))

        console.print(tabla)
        return

    # 👉 3) Email con output (respuesta generada)
    if tipo == "email_output" and "output" in contenido:
        texto = contenido["output"]
        console.print("[bold cyan]📧 Resultado:[/bold cyan]")
        console.print(f"[italic]{texto}[/italic]\n")

        # Guardar archivo
        try:
            descargas = obtener_ruta_descargas()
            path = os.path.join(descargas, f"Email_{int(time.time())}.txt")
            with open(path, "w", encoding="utf-8") as f:
                f.write(texto)

            console.print(f"[bold green]✔ Confirmación guardada en:[/bold green] [cyan]{path}[/cyan]\n")
        except Exception as e:
            console.print(f"[bold red]❌ Error al guardar archivo:[/bold red] {e}")

        return

    # 👉 4) Tablas
    if tipo == "tabla" and isinstance(contenido, list):
        imprimir_tabla(contenido)
        guardar_excel(contenido, "Reporte_Datos")
        guardar_csv(contenido, "Reporte_Datos")
        return

    # Fallback
    console.print(f"[cyan]{contenido}[/cyan]")


# ======================================================
# 🧠 LOOP PRINCIPAL
# ======================================================

def main():
    banner()
    bienvenida()

    while True:
        consulta = input("💬 Escribí tu consulta: ").strip()

        if consulta.lower() in ("salir", "exit", "quit"):
            console.print("\n👋 [bold cyan]¡Saliendo del sistema![/bold cyan]")
            break

        if not consulta:
            console.print("[bold red]⚠ Ingresá una consulta válida.[/bold red]")
            continue

        esperar_respuesta()
        respuesta = enviar_a_n8n({"query": consulta})
        procesar_respuesta(respuesta)

        input("\nENTER para nueva consulta...")

if __name__ == "__main__":
    main()
