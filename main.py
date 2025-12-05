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
        # Windows: C:\Users\Usuario\Desktop
        desktop = os.path.join(home, "Desktop")
        return desktop if os.path.exists(desktop) else home
    else:
        # Linux/Mac: ~/Desktop o ~/Descargas
        desktop = os.path.join(home, "Desktop")
        descargas = os.path.join(home, "Descargas")
        if os.path.exists(desktop):
            return desktop
        elif os.path.exists(descargas):
            return descargas
        return home

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

    first = datos[0]
    for col in first.keys():
        table.add_column(col.capitalize())

    for row in datos:
        table.add_row(*[str(v) for v in row.values()])

    console.print(table)


def guardar_excel(datos, nombre="Reporte"):
    """Guarda datos en archivo Excel en la carpeta de descargas del usuario"""
    try:
        df = pd.DataFrame(datos)
        descargas = obtener_ruta_descargas()
        output_path = os.path.join(descargas, f"{nombre}_{int(time.time())}.xlsx")
        df.to_excel(output_path, index=False)
        return output_path
    except Exception as e:
        console.print(f"[bold red]❌ Error al guardar Excel:[/bold red] {e}")
        return None


def guardar_csv(datos, nombre="Reporte"):
    """Guarda datos en archivo CSV en la carpeta de descargas del usuario"""
    try:
        df = pd.DataFrame(datos)
        descargas = obtener_ruta_descargas()
        output_path = os.path.join(descargas, f"{nombre}_{int(time.time())}.csv")
        df.to_csv(output_path, index=False)
        return output_path
    except Exception as e:
        console.print(f"[bold red]❌ Error al guardar CSV:[/bold red] {e}")
        return None


def detectar_tipo_respuesta(contenido):
    """Detecta si la respuesta es de email, SQL o datos generales"""
    if isinstance(contenido, dict):
        claves = [k.lower() for k in contenido.keys()]
        if any(x in claves for x in ["email", "correo", "mail", "mensaje", "asunto"]):
            return "email"
    
    if isinstance(contenido, list) and len(contenido) > 0:
        if isinstance(contenido[0], dict):
            claves = [k.lower() for k in contenido[0].keys()]
            if any(x in claves for x in ["email", "correo", "mail", "nombre", "teléfono", "dhi"]):
                return "email"
    
    return "generic"


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

    tipo_respuesta = detectar_tipo_respuesta(contenido)

    # Texto simple
    if isinstance(contenido, str):
        console.print("[bold cyan]" + contenido.capitalize() + "[/bold cyan]")
        return 
    
    # Datos en tabla (lista de registros)
    if isinstance(contenido, list):
        imprimir_tabla(contenido)
        
        # Detectar tipo de datos para nombrar el reporte
        nombre_reporte = "Reporte_Correos" if tipo_respuesta == "email" else "Reporte_Datos"
        
        try:
            console.print("\n[bold yellow]📁 Generando archivo Excel...[/bold yellow]")
            path = guardar_excel(contenido, nombre_reporte)
            if path:
                console.print(f"[bold green]✔ Excel guardado:[/bold green] {path}")
        except Exception as e:
            console.print("[bold red]❌ Error al generar Excel:[/bold red]", e)
        
        try:
            console.print("[bold yellow]📁 Generando archivo CSV...[/bold yellow]")
            path_csv = guardar_csv(contenido, nombre_reporte)
            if path_csv:
                console.print(f"[bold green]✔ CSV guardado:[/bold green] {path_csv}")
        except Exception as e:
            console.print("[bold red]❌ Error al generar CSV:[/bold red]", e)
        return
    
    # Datos en diccionario (email único o resultado único)
    if isinstance(contenido, dict) and tipo_respuesta == "email":
        console.print("[bold green]📧 Datos de Correo:[/bold green]")
        table = Table(show_header=True, header_style="bold cyan")
        table.add_column("Campo", style="cyan")
        table.add_column("Valor", style="magenta")
        
        for key, value in contenido.items():
            table.add_row(str(key).upper(), str(value)[:80])  # Limitar longitud de valores
        
        console.print(table)
        
        # Guardar como CSV
        try:
            path_csv = guardar_csv([contenido], "Reporte_Email")
            if path_csv:
                console.print(f"[bold green]✔ CSV guardado:[/bold green] {path_csv}")
        except Exception as e:
            console.print("[bold red]❌ Error al generar CSV:[/bold red]", e)
        return
    
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
