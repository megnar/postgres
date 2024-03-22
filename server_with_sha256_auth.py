import socket

def simulate_postgresql_server():
    # Создаем сокет для TCP-сервера
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 5433))  # Привязываем к порту 5432, который обычно используется PostgreSQL
    server_socket.listen(1)  # Ожидаем только одно соединение

    print("Сервер PostgreSQL запущен.")

    # Принимаем соединение от клиента
    client_socket, client_address = server_socket.accept()
    print(f"Подключен клиент: {client_address}")

    port_bytes = int(client_address[1]).to_bytes(2, "big")
    packet = b'N'
    packet2 = b'R\x00\x00\x00\x17\x00\x00\x00\nSCRAM-SHA-256\x00\x00' 
    packet3_first_part = b'R\x00\x00\x00\\\x00\x00\x00\x0br='
    packet3_second_part = b',s=9v2tearEZ7T+3ljGywrtQQ==,i=4096'
    packet4 = b'R\x00\x00\x006\x00\x00\x00\x0cv=kjvcwoaIqAsP32NJalNu1aezDiauZNC/K7ceFD0Vzyw=R\x00\x00\x00\x08\x00\x00\x00\x00S\x00\x00\x00\x17in_hot_standby\x00off\x00S\x00\x00\x00\x19integer_datetimes\x00on\x00S\x00\x00\x00\x15TimeZone\x00Etc/UTC\x00S\x00\x00\x00\x1bIntervalStyle\x00postgres\x00S\x00\x00\x00\x14is_superuser\x00on\x00S\x00\x00\x00\x16application_name\x00\x00S\x00\x00\x00&default_transaction_read_only\x00off\x00S\x00\x00\x00\x1ascram_iterations\x004096\x00S\x00\x00\x00\x17DateStyle\x00ISO, MDY\x00S\x00\x00\x00#standard_conforming_strings\x00on\x00S\x00\x00\x00 session_authorization\x00admin\x00S\x00\x00\x00\x19client_encoding\x00UTF8\x00S\x00\x00\x002server_version\x0016.2 (Debian 16.2-1.pgdg120+2)\x00S\x00\x00\x00\x19server_encoding\x00UTF8\x00K\x00\x00\x00\x0c\x00\x00\x08\xe4\xada\xacAZ\x00\x00\x00\x05I'

        # Добавьте остальные пакеты здесь...

    try:
        response = client_socket.recv(1024)
        print("Ответ от клиента:", response)

        
        client_socket.send(packet)
        print("Отправлен пакет 1:", packet)
        
        response = client_socket.recv(1024)
        print("Ответ от клиента:", response)



        client_socket.send(packet2)
        print("Отправлен пакет 2:", packet)
        response = client_socket.recv(1024)
        print("Ответ от клиента:", response)


        r_string = response.split(b'r=')[1] + response.split(b'r=')[1]
        packet3 = packet3_first_part + r_string + packet3_second_part
        client_socket.send(packet3)
        print("Отправлен пакет 3:", packet)
        response = client_socket.recv(1024)
        print("Ответ от клиента:", response)

        client_socket.send(packet4)
        print("Отправлен пакет 4:", packet4)
        response = client_socket.recv(1024)
        print("Ответ от клиента:", response)


    finally:
        # Закрываем сокеты
        client_socket.close()
        server_socket.close()

if __name__ == "__main__":
    # Замените packets на список перехваченных пакетов Wireshark
    

    # Запускаем сервер с перехваченными пакетами
    simulate_postgresql_server()

