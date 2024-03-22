import logging
import psycopg2
from psycopg2 import extensions
import socket


# Настройка логирования
logging.basicConfig(level=logging.DEBUG, filename="/Users/evgeny/Desktop/PycharmProjects/work/mock/test_client_server/logfile.log")
logger = logging.getLogger(__name__)

class MyConnection(extensions.connection):
    def send(self, data):
        print("dfg")
        logger.debug(f"Sent: {data}")
        return super().send(data)

    def recv(self, size):
        print("rec")
        data = super().recv(size)
        logger.debug(f"Received: {data}")
        return data
    

def get_current_port():
    # Создаем сокет
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Привязываем его к любому доступному адресу и случайному порту
    sock.bind(('localhost', 0))
    # Получаем информацию о привязанном адресе и порте
    _, port = sock.getsockname()
    # Закрываем сокет
    sock.close()
    return port


if __name__ == "__main__":
    port = get_current_port()
    print("Моя программа работает на порту:", port)
    port = get_current_port()
    print("Моя программа работает на порту:", port)
    port = get_current_port()
    print("Моя программа работает на порту:", port)


    # Установка фабрики соединений
    psycopg2.extensions.connection_factory = MyConnection

    # Создание соединения
    conn = psycopg2.connect(
            dbname="test_db",
            user="admin",
            password="admin",
            host="0.0.0.0",
            port="5432"
        )

    print(psycopg2.extensions.connection_factory)
    cur = conn.cursor()
    logger.debug(f"Sent:")
    cur.execute("select 1")
    rows = cur.fetchall()
    print(rows)
    cur.close()
    conn.close()