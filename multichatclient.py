import socket
import threading
import sys
import os

# Clase para estilos y colores


class Estilos:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# Función para imprimir mensajes con color y estilo


def clear_and_display_header():
    os.system('cls' if os.name == 'nt' else 'clear')
    imprimir_mensaje("Chat Multicanal - Terminal de Usuario", Estilos.WARNING)


def imprimir_mensaje(mensaje, estilo=Estilos.OKGREEN):
    print(f"{estilo}{mensaje}{Estilos.ENDC}")


# Inicio de la interfaz del usuario
clear_and_display_header()
HOST = input(
    f'{Estilos.BOLD}Ingresa la dirección IP del servidor: {Estilos.ENDC}')
PORT = int(
    input(f'{Estilos.BOLD}Ingresa el puerto del servidor: {Estilos.ENDC}'))

# Configuración del cliente para conectarse al servidor
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    client.connect((HOST, PORT))
except Exception as e:
    imprimir_mensaje(f"No se pudo conectar al servidor: {e}", Estilos.FAIL)
    sys.exit()

clear_and_display_header()
imprimir_mensaje(
    "Conectado al servidor.", Estilos.OKBLUE)
imprimir_mensaje("Escribe 'exit' para salir.", Estilos.WARNING)

running = True


def send_message():
    global running
    while running:
        message = input()
        client.sendall(message.encode('utf-8'))

        if message == 'exit':
            running = False


def receive_message():
    global running
    while running:
        try:
            message = client.recv(1024).decode('utf-8')
            if message:
                imprimir_mensaje(message,  Estilos.HEADER)
            if message == 'exit':
                running = False
        except Exception as e:
            imprimir_mensaje(f"Error al recibir mensaje: {e}", Estilos.FAIL)
            running = False


thread_send = threading.Thread(target=send_message)
thread_receive = threading.Thread(target=receive_message)

thread_receive.start()
thread_send.start()

thread_send.join()
thread_receive.join()

client.close()
imprimir_mensaje("Conexión cerrada. Adiós!", Estilos.HEADER)
