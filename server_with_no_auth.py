import socket
import asyncio

def create_authentificattion(client_socket):
    packet = b'N'
    packet4 = b'R\x00\x00\x00\x08\x00\x00\x00\x00S\x00\x00\x00\x16application_name\x00\x00S\x00\x00\x00\x19client_encoding\x00UTF8\x00S\x00\x00\x00\x17DateStyle\x00ISO, MDY\x00S\x00\x00\x00&default_transaction_read_only\x00off\x00S\x00\x00\x00\x17in_hot_standby\x00off\x00S\x00\x00\x00\x19integer_datetimes\x00on\x00S\x00\x00\x00\x1bIntervalStyle\x00postgres\x00S\x00\x00\x00\x15is_superuser\x00off\x00S\x00\x00\x00\x19server_encoding\x00UTF8\x00S\x00\x00\x00$server_version\x0014.11 (Homebrew)\x00S\x00\x00\x00 session_authorization\x00admin\x00S\x00\x00\x00#standard_conforming_strings\x00on\x00S\x00\x00\x00\x1bTimeZone\x00Europe/Moscow\x00K\x00\x00\x00\x0c\x00\x01c\xea?\xbe\x0b\xa5Z\x00\x00\x00\x05I'
    packet5 = b'C\x00\x00\x00\nBEGIN\x00Z\x00\x00\x00\x05T' 

    response = client_socket.recv(1024)
    print("Ответ от клиента:", response)

    client_socket.send(packet)
    print("Отправлен пакет 1:", packet)
    response = client_socket.recv(1024)
    print("Ответ от клиента:", response)

    client_socket.send(packet4)
    print("Отправлен пакет 4:", packet4)
    response = client_socket.recv(1024)
    print("Ответ от клиента:", response)

    client_socket.send(packet5)
    print("Отправлен пакет 5:", packet5)
    response = client_socket.recv(1024)
    print("Ответ от клиента:", response)    


def select_data_row(fields: list):
    answer = b'D'
    num_fields = len(fields)
    length = 6 + num_fields * 4
    for field in fields:
        length += len(str(field))
    length_as_bytes = length.to_bytes(4, "big")
    num_fields_as_bytes = num_fields.to_bytes(2, "big")
    answer += length_as_bytes + num_fields_as_bytes
    for field in fields:
        field_length = len(str(field))
        answer += field_length.to_bytes(4, "big") + str(field).encode("utf-8")
    return answer

def select_row_description(fields: list):
    answer = b'T'
    num_fields = len(fields)
    length = 6 + num_fields * 19  
    for field in fields:
        length += len(str(field))
    length_as_bytes = length.to_bytes(4, "big")
    num_fields_as_bytes = num_fields.to_bytes(2, "big")
    answer += length_as_bytes + num_fields_as_bytes
    for index, field in enumerate(fields):
        answer += str(field).encode("utf-8") + b'\x00'
        answer += b'\x00\x00@\x02'
        answer += (index + 1).to_bytes(2, "big")
        answer += b'\x00\x00\x04\x13'
        answer += b'\xff\xff'
        answer += b'\x00\x00\x00h'
        answer += b'\x00\x00'
    return answer

def return_select_query(row_names: list, rows: list):
    answer = select_row_description(row_names)
    for row in rows:
        answer += select_data_row(row)
    answer += b'C\x00\x00\x00\rSELECT 4\x00' # complete_value
    answer += b'Z\x00\x00\x00\x05T' # ready_for_query
    return answer


async def clients_working(client_socket):
    pack6 = return_select_query(["?column?"], [[1]])
    packet7 = return_select_query(["names", "age"], [["John", 38], ["Dima", 27]])

    try:
        create_authentificattion(client_socket)
        
        client_socket.send(pack6)
        print("Отправлен пакет 6:", pack6)
        #await client_socket.drain()
        response = client_socket.recv(1024)
        print("Ответ от клиента:", response)

        client_socket.send(packet7)
        print("Отправлен пакет 7:", packet7)
        response = client_socket.recv(1024)
        print("Ответ от клиента:", response)

    finally:
        client_socket.close()


async def simulate_postgresql_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        server_socket.bind(('localhost', 5435))
        server_socket.listen(100) 

        print("Сервер запущен")
        
        while True:
            client_socket, client_address = server_socket.accept()
            print(f"Подключен клиент: {client_address}")
            await clients_working(client_socket)

    finally:
        server_socket.close()


    
asyncio.run(simulate_postgresql_server())
# if __name__ == "__main__":
#     simulate_postgresql_server()

