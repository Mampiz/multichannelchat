import socket
import threading

HOST = 'localhost'
PORT = 6667
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
connections = []
channels = []
default_channel = "general"
current_channels = {}

# Funció que controla les conexions i la direcció de canals


def handle_client(conn, addr):
    print(f"[Nueva Conexión] {addr} se ha conectado al servidor.")
    conn.sendall("Ingrese su nombre de usuario:".encode('utf-8'))
    username = conn.recv(1024).decode('utf-8')
    connections.append((conn, username))

    # Enviar un mensaje de bienvenida con los comandos disponibles
    welcome_message = (
        "Bienvenido al chat. Comandos disponibles:\n"
        "CREATE <nombre_canal> - Crea un nuevo canal.\n"
        "MOVE <nombre_canal> - Cambia al canal especificado.\n"
        "DEL <nombre_canal> - Elimina el canal especificado.\n"
        "PRIV <nombre_usuario> <mensaje> - Envia un mensaje privado a un usuario.\n"
        "CHANNELS - Muestra la lista de canales disponibles.\n"
        "USERS - Muestra los usuarios en el canal actual.\n"
        "ALL - Muestra todos los usuarios y los canales en los que están.\n"
        "HELP - Muestra esta ayuda.\n"
        "Cree o muevase a un canal para empezar a chatear\n"
    )
    conn.sendall(welcome_message.encode('utf-8'))
    show_all_user_list(conn)

    while True:
        message = conn.recv(1024).decode('utf-8')
        if message.startswith("CREATE"):
            channel_name = message.split(" ")[1]
            create_channel(channel_name, conn)
        elif message.startswith("DEL"):
            channel_name = message.split(" ")[1]
            delete_channel(channel_name, conn)
        elif message.startswith("MOVE"):
            channel_name = message.split(" ")[1]
            change_channel(channel_name, conn)
        elif message.startswith("PRIV"):
            xseparation = message.split(" ")
            xusername = xseparation[1]
            xmessage = " ".join(xseparation[2:])
            send_private_message(xusername, xmessage, conn)
        elif message == "CHANNELS":
            show_channel_list(conn)
        elif message == "USERS":
            show_user_list(conn)
        elif message == "ALL":
            show_all_user_list(conn)
        elif message.lower() == "help":
            conn.sendall(welcome_message.encode('utf-8'))
        else:
            send_message_to_channel(f'[{get_username(conn)}]: {message}', conn)


def remove_from_current_channels(client):
    channel = current_channels.get(client)
    if channel:
        del current_channels[client]
        send_message_to_channel(
            f'{get_username(client)} se ha eliminado del canal', client)


def get_username(client):
    for conn, username in connections:
        if conn == client:
            return username
    return None


def create_channel(channel_name, client):
    if channel_name in channels:
        client.sendall(
            f'El canal "{channel_name}" ya existe'.encode('utf-8'))
    else:
        channels.append(channel_name)
        current_channels[client] = channel_name
        client.sendall(
            f'Canal "{channel_name}" creado correctamente'.encode('utf-8'))


def delete_channel(channel_name, client):
    if channel_name in channels:
        if current_channels[client] == channel_name:
            channels.remove(channel_name)
            del current_channels[client]
            client.sendall(
                f'Canal "{channel_name}" eliminado correctamente'.encode('utf-8'))
            send_message_to_channel(
                f'El canal "{channel_name}" ha sido eliminado por {get_username(client)}', client)
        else:
            client.sendall(
                f'No tienes permisos para eliminar el canal "{channel_name}"'.encode('utf-8'))
    else:
        client.sendall(
            f'El canal "{channel_name}" no existe'.encode('utf-8'))


def change_channel(channel_name, client):
    if channel_name in channels:
        current_channel = current_channels.get(client)
        if current_channel != channel_name:
            if current_channel:
                send_message_to_channel(
                    f'{get_username(client)} ha salido', client)
            current_channels[client] = channel_name
            client.sendall(
                f'Te has movido al canal "{channel_name}"'.encode('utf-8'))
            send_message_to_channel(
                f'{get_username(client)} se ha movido a "{channel_name}"', client)
        else:
            client.sendall(
                f'Ya estas en el canal "{channel_name}"'.encode('utf-8'))
    else:
        client.sendall(
            f'El canal "{channel_name}" no existe'.encode('utf-8'))

# Funció per enviar misatjes als altres clients del canal


def send_message_to_channel(message, client):
    channel = current_channels.get(client)
    if channel:
        for conn, client_channel in current_channels.items():
            if client_channel == channel and conn != client:
                conn.sendall(message.encode('utf-8'))

# Funció per enviar misatje privat a client, pot estar al mateix o en un canal diferent


def send_private_message(recipient_username, message, client):
    for conn, username in connections:
        if username == recipient_username:
            conn.sendall(
                f'[Mensaje privado de {get_username(client)}]: {message}'.encode('utf-8'))
            break
    else:
        client.sendall(
            f'L\'usuario "{recipient_username}" no esta conectado'.encode('utf-8'))

# Funció per enseñar la llista de canals


def show_channel_list(client):
    channel_list = ', '.join(channels)
    client.sendall(f'Canales disponibles: {channel_list}'.encode('utf-8'))

# Funció per enseñar la llista de usuaris


def show_user_list(client):
    channel = current_channels.get(client)
    if channel:
        users = []
        for conn, username in connections:
            if current_channels.get(conn) == channel:
                users.append(username)
        user_list = ', '.join(users)
        client.sendall(
            f'Usuarios en el canal "{channel}": {user_list}'.encode('utf-8'))
    else:
        client.sendall(f'No estas en ningun canal'.encode('utf-8'))


def show_all_user_list(client):
    user_list = ""
    for channel in channels:
        channel_users = []
        for conn, username in connections:
            if current_channels.get(conn) == channel:
                channel_users.append(username)
        users = ", ".join(channel_users)
        user_list += f'Usuarios en el canal "{channel}": {users}\n'
    client.sendall(user_list.encode('utf-8'))


def send_message():
    while True:
        message = input()
        send_message_to_channel(f'[SERVIDOR]: {message}', None)

# Funció de configuració e inici del servidor


def start_server():
    server.listen()
    print(f"[Datos del servidor] IP: {HOST} i Port: {PORT}")
    thread_send = threading.Thread(target=send_message)
    thread_send.start()
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()


print("[SERVIDOR INICIADO]")
start_server()
