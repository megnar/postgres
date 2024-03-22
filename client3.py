import socket

# Адрес и порт сервера
server_address = ('127.0.0.1', 5433)

# Создание сокета TCP
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    # Подключение к серверу
    client_socket.connect(server_address)

    # Отправка данных на сервер
    message = "Hello, server!"
    client_socket.sendall(message.encode())

    # Получение ответа от сервера
    data = client_socket.recv(1024)
    print("Received:", data.decode())

finally:
    # Закрытие соединения
    client_socket.close()
