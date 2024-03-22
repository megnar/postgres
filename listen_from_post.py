import socket

# Адрес и порт сервера
server_address = ('127.0.0.1', 5432)

# Создание сокета TCP
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    # Подключение к серверу
    client_socket.connect(server_address)

    # Отправка данных на сервер
    packet = b'\x00\x00\x00\x08\x04\xd2\x16/'
    client_socket.send(packet)

    # Получение ответа от сервера
    data = client_socket.recv(1024)
    print("Received:", data)

    packet = b'\x00\x00\x00%\x00\x03\x00\x00user\x00admin\x00database\x00test_db\x00\x00'
    client_socket.send(packet)

    # Получение ответа от сервера
    data = client_socket.recv(1024)
    print("Received:", data)

    packet = b'p\x00\x00\x006SCRAM-SHA-256\x00\x00\x00\x00 n,,n=,r=0QxP5oFgrBkODRPusBB2j8T9'
    client_socket.send(packet)

    # Получение ответа от сервера
    data = client_socket.recv(1024)
    print("Received:", data)


finally:
    # Закрытие соединения
    client_socket.close()
