import socket
import time

from Packet import Packet
from client_packets.ClientHandshakePacket import ClientHandshakePacket
from client_packets.ClientRequestPacket import ClientRequestPacket


def pingServer(ip, port: int):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:

            s.connect((ip, port))
            s.sendall(ClientHandshakePacket(server_addr=ip, server_port=port, next_state=1).encode())
            s.sendall(ClientRequestPacket().encode())
            time.sleep(0.3)
            length = Packet.read_varint(s)
            data = s.recv(length)
            return data[5:400].decode()
       # except Exception as e:
            #print(e)
            #return 0