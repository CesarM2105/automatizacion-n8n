# 🎭 Sistema Inteligente de Boletería – Artechito 2025  
Consultas inteligentes con IA sobre una base de datos teatral operando sobre PostgreSQL (Supabase) y automatizada con n8n.

---

## 📘 Introducción Técnica

Este repositorio contiene el **cliente Python** que se comunica con el flujo de automatización en **n8n**.  
Su función es actuar como **interfaz de usuario**, permitiendo realizar consultas en lenguaje natural sobre la boletería del teatro y obtener:

- texto generado por IA  
- tablas procesadas  
- archivos Excel / CSV automáticos  
- archivos de texto generado por IA  
- datos para envío de email o subida a Drive  

El flujo completo opera así:
Usuario → Python → n8n (IA + SQL + Automatización) → Supabase → Python


---

# 📑 Índice

1. Arquitectura general  
2. Estructura del repositorio  
3. Funcionamiento del código  
4. Explicación técnica del archivo `main.py`  
5. Explicación técnica de `api_client.py`  
6. Librerías utilizadas y razones técnicas  
7. Manejo de errores  
8. Flujo completo Python → n8n → Supabase  
9. Posibles mejoras  
10. Equipo Artechito  

---

# 🧩 1. Arquitectura General

El sistema está dividido en 3 capas:

### **A) Cliente Python (este repositorio)**
- Recibe consultas del usuario  
- Envía el prompt a n8n  
- Procesa respuestas  
- Genera Excel, CSV, tablas y archivos  
- Presenta una UI limpia con Rich  

### **B) n8n (Automatización)**
- Interpreta lenguaje natural con IA (Gemini)  
- Genera SQL seguro para Supabase  
- Maneja creación de archivos, emails y Drive  
- Devuelve la respuesta ya procesada a Python  

### **C) Supabase (Base de Datos)**
- Base PostgreSQL real  
- Contiene obras, funciones, salas, clientes, ventas  
- Es consultada exclusivamente con SELECT seguros  

---

# 🗂️ 2. Estructura del repositorio



automatizacion-n8n/
│── main.py # Programa principal de consola
│── modules/
│ └── api_client.py # Cliente HTTP que envía requests a n8n
│── requirements.txt # Dependencias del sistema

---

# 🧠 3. Funcionamiento del sistema

1. El usuario escribe una consulta en lenguaje natural.  
2. Python envía el JSON al webhook protegido de n8n.  
3. n8n:
   - interpreta la intención,  
   - construye SQL seguro,  
   - ejecuta en Supabase,  
   - genera archivos si corresponde.  
4. Python recibe la respuesta estructurada.  
5. Python:
   - imprime tablas  
   - guarda Excel/CSV  
   - guarda archivos de email  
   - muestra texto formateado  

El cliente Python está diseñado para **no depender de la estructura interna del workflow**, lo que lo hace robusto y escalable.

---

# 🧱 4. Explicación Técnica del `main.py`

El archivo `main.py` implementa:

---

## ✔ Detección automática de rutas de descarga

```python
obtener_ruta_descargas()

Funciona en:

Windows

Mac

Linux

Prioriza Escritorio o Descargas, garantizando portabilidad.

✔ UI limpia con Rich

Funciones:

banner() → limpia y muestra el título

bienvenida() → instrucciones

imprimir_tabla() → renderiza una tabla profesional

esperar_respuesta() → spinner animado estilo “Procesando…”

Razón técnica: Rich da un soporte visual profesional sin depender de GUI externa.

✔ Exportación automática a Excel y CSV
guardar_excel()
guardar_csv()


Usan pandas para:

crear DataFrame

exportar Excel/CSV

generar nombres únicos con timestamp

Motivo: pandas es estable, rápido y estándar empresarial.

✔ Detector inteligente de tipo de respuesta
detectar_tipo_respuesta()


Analiza si la respuesta de n8n contiene:

texto

tabla (lista de dicts)

email

email_output

fallback

Esto evita depender de estructuras específicas.
Permite que n8n evolucioné sin modificar Python.

✔ Procesador de respuesta
procesar_respuesta()


Encargado de:

interpretar JSON

mostrar texto limpio

generar archivos

imprimir tablas

manejar emails

fallback de errores

Es el módulo más importante del cliente.

✔ Loop principal
main()


Características:

lectura continua

manejo de “salir/exit/quit”

validación de entrada

envío a n8n

respuesta formateada

🧩 5. Explicación técnica del api_client.py

Este módulo encapsula toda la comunicación HTTP.

enviar_a_n8n()

Utiliza:

requests.post()


Con:

JSON como body

autenticación básica

manejo de errores homogéneo

tiempo de espera alto para consultas complejas

Motivo:
Separar la lógica de UI y la lógica de red mejora la mantenibilidad del código.

🧰 6. Librerías utilizadas y por qué
| Librería        | Uso               | Por qué se eligió            |
| --------------- | ----------------- | ---------------------------- |
| `requests`      | cliente HTTP      | simple, robusto, estándar    |
| `pandas`        | Excel / CSV       | potente y maduro             |
| `rich`          | UI en consola     | tablas limpias y profesional |
| `dotenv`        | cargar variables  | seguridad y buenas prácticas |
| `os / platform` | rutas del sistema | multiplataforma              |
| `json`          | parsing de n8n    | estructura estándar          |
| `time`          | timestamp         | garantizan nombres únicos    |

🛡 7. Manejo de errores

Implementado en todo el sistema:

desconexión de red

JSON corrupto

errores HTTP

errores en Excel o CSV

respuestas inesperadas de n8n

Devuelve siempre:

{"error": "mensaje"}


Evita que la aplicación se caiga.

🔄 8. Flujo completo Python → n8n → Supabase

1. Python envía {"query": "..."} a n8n.
2. n8n decide intención (IA Agent).
3. Se genera SQL seguro.
4. Supabase ejecuta la consulta.
5. n8n procesa salidas:
   - Excel
   - CSV
   - Email
   - Drive
   - Texto
6. Python recibe JSON final y lo presenta.

🚀 9. Posibles mejoras

CLI basada en Typer

Logs persistentes

Exportación a PDF

Configuración editable YAML

Autocomplete de consultas

👥 10. Créditos

Desarrolladores del código Python:
Mauricio Cuellar & César Mendoza
