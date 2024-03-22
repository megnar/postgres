import psycopg2
from scapy.all import * #TODO: syntax


def create_postgresql_request_packet():
    packet = IP(dst="127.0.0.1") / TCP(dport=5433, sport=49183) / Raw(load="")
    
    return packet

# Отправка пакета
def send_packet(packet):
    send(packet)

def packet_handler(packet):
    if packet.haslayer(TCP) and packet.haslayer(Raw):
        tcp_packet = packet[TCP]
        raw_payload = packet[Raw].load.decode('utf-8')
        print(f"Received TCP packet from {packet[IP].src} on port {tcp_packet.sport}:")
        print(f"Payload: {raw_payload}")




if __name__ == '__main__':
    packet = create_postgresql_request_packet()
    send_packet(packet)
    
#     ip_packet = IP(src="127.0.0.1", dst="127.0.0.1")

#     tcp_packet = TCP(sport=49823, dport=5432, flags="S", seq=2992324088, window=65535, options=[("MSS", 16344), ("NOP", None), ("WScale", 6), ("NOP", None), ("NOP", None), ("Timestamp", (909698602, 0)), ("SACK", None)])

# # Отправляем пакет
#     send(ip_packet/tcp_packet)
