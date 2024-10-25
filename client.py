from flask import Flask, render_template, request, jsonify
import socket
import threading

app = Flask(__name__)

# Параметры подключения к серверу
HOST = '192.168.50.235'  # IP сервера в локальной сети
PORT = 12345           # Порт сервера

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

messages = []

def send_message(message):
    client_socket.send(message.encode("utf-8"))

def receive_messages():
    while True:
        try:
            message = client_socket.recv(1024).decode("utf-8")
            messages.append(message)
        except:
            break

# Старт потока для получения сообщений
threading.Thread(target=receive_messages, daemon=True).start()

@app.route("/")
def chat():
    return render_template("chat.html")

@app.route("/send", methods=["POST"])
def send():
    message = request.form["message"]
    send_message(message)
    return "Сообщение отправлено"

@app.route("/get_messages", methods=["GET"])
def get_messages():
    return jsonify({"messages": messages})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
