import socket
import threading

# Параметры сервера
HOST = '192.168.50.235'  # Укажите IP-адрес сервера в локальной сети
PORT = 12345           # Порт для подключения

clients = []

def handle_client(client_socket, client_address):
    while True:
        try:
            message = client_socket.recv(1024).decode("utf-8")
            if message:
                print(f"{client_address} говорит: {message}")
                broadcast_message(message, client_socket)
            else:
                remove_client(client_socket)
                break
        except:
            remove_client(client_socket)
            break

def broadcast_message(message, sender_socket):
    for client in clients:
        if client != sender_socket:
            try:
                client.send(message.encode("utf-8"))
            except:
                remove_client(client)

def remove_client(client_socket):
    if client_socket in clients:
        clients.remove(client_socket)

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(2)
    print(f"Сервер запущен на {HOST}:{PORT}")

    while True:
        client_socket, client_address = server_socket.accept()
        clients.append(client_socket)
        print(f"Новое подключение: {client_address}")

        client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
        client_thread.start()

if __name__ == "__main__":
    start_server()
