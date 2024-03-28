import socket
import asyncio    


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



def return_error_query(severity = "ERROR", text = "ERROR", code = "P0001", message = "raised exception" ):
    answer = b'E'
    total_length = len(text) + len(severity) + len(code) + len(message) + 58
    print("размер ошибки ерр", total_length)
    length_as_bytes = total_length.to_bytes(4, "big")
    answer += length_as_bytes
    answer += b'S' + severity.encode("utf-8") + b'\x00'
    answer += b'V' + text.encode("utf-8") + b'\x00'
    answer += b'C' + code.encode("utf-8") + b'\x00'
    answer += b'M' + message.encode("utf-8") + b'\x00'
    answer += b'P15\x00Fparse_relation.c\x00L1384\x00RparserOpenTable\x00\x00'
    print(len(answer))
    return answer

async def create_authentificattion(reader, writer):
    packet_auth_1 = b'N'
    packet_auth_2 = b'R\x00\x00\x00\x08\x00\x00\x00\x00S\x00\x00\x00\x16application_name\x00\x00S\x00\x00\x00\x19client_encoding\x00UTF8\x00S\x00\x00\x00\x17DateStyle\x00ISO, MDY\x00S\x00\x00\x00&default_transaction_read_only\x00off\x00S\x00\x00\x00\x17in_hot_standby\x00off\x00S\x00\x00\x00\x19integer_datetimes\x00on\x00S\x00\x00\x00\x1bIntervalStyle\x00postgres\x00S\x00\x00\x00\x15is_superuser\x00off\x00S\x00\x00\x00\x19server_encoding\x00UTF8\x00S\x00\x00\x00$server_version\x0014.11 (Homebrew)\x00S\x00\x00\x00 session_authorization\x00admin\x00S\x00\x00\x00#standard_conforming_strings\x00on\x00S\x00\x00\x00\x1bTimeZone\x00Europe/Moscow\x00K\x00\x00\x00\x0c\x00\x01c\xea?\xbe\x0b\xa5Z\x00\x00\x00\x05I'
    packet_auth_3 = b'C\x00\x00\x00\nBEGIN\x00Z\x00\x00\x00\x05T' 
    await reader.read(1024)
    writer.write(packet_auth_1)
    await reader.read(1024)
    writer.write(packet_auth_2)
    await reader.read(1024)
    writer.write(packet_auth_3)
    

async def handle_client(reader, writer):
    packet6 = return_select_query(["?column?"], [[1]])
    packet7 = return_select_query(["names", "age"], [["John", 38], ["Dima", 27]])
    packet8 = return_error_query()

    try:
        await create_authentificattion(reader, writer)
        
        await reader.read(1024)
        writer.write(packet6)
        await writer.drain()


        await reader.read(1024)
        writer.write(packet7)
        await writer.drain()

        response = await reader.read(1024)
        writer.write(packet8)
        await writer.drain()
        writer.write(b"Z\x00\x00\x00\x05E")
        print("Отправлена ошибка")
        response = await reader.read(1024)
        print("Ответ от клиента:", response)

    finally:
        writer.close()

async def main():
    server = await asyncio.start_server(handle_client, 'localhost', 5435)
    async with server:
        print('Сервер запущен на', server.sockets[0].getsockname())
        await server.serve_forever()

asyncio.run(main())


