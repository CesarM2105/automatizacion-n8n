from modules.db import load_data
# from modules.chat import procesar_consulta
from modules.api_client import enviar_a_n8n

def main():
    obras, salas, entradas = load_data()
    print("🎭 Bienvenido al sistema de boletería inteligente\n")

    while True:
        try:
            user = input("👉 Escribí tu consulta (o 'salir'): ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nSaliendo...")
            break

        if user.lower() == "salir":
            break

        # respuesta_local = procesar_consulta(user, obras, entradas)
        if True:
            print("Enviando a n8n...")
            resp = enviar_a_n8n(user)
            print(resp)


if __name__ == "__main__":
    main()