from abc import ABC, abstractmethod
import json
class Packet(ABC):
    def __init__(self, packet_id):
        self.packet_id = packet_id

    @abstractmethod
    def encode(self):
        pass
    @staticmethod
    def readString(self, sock: socket.socket):
        string_length = Packet.read_varint(sock)
        server_address = self.socket.recv(string_length).decode("utf-8")
        return server_address
    @staticmethod
    def read_varint(sock):
        num = 0
        shift = 0
        while True:
            byte = sock.recv(1)
            if not byte:
                raise ConnectionError("Połączenie przerwane")
            b = byte[0]
            num |= (b & 0x7F) << shift
            if not (b & 0x80):
                break
            shift += 7
            if shift >= 32:
                raise ValueError("VarInt jest za duży")
        return num
    @staticmethod
    def encode_varint(n):
        result = bytearray()
        while True:
            byte = n & 0x7F
            n >>= 7
            if n != 0:
                byte |= 0x80
                result.append(byte)
            else:
                result.append(byte)
                break
        return result
    @staticmethod
    def write_chat_component(dictionary: dict):
        json_parsing = json.dumps(dictionary)
        json_bytes = json_parsing.encode("utf-8")
        return json_bytes
    @staticmethod
    def write_string(text):
        text_bytes = text.encode("utf-8")
        return Packet.encode_varint(len(text_bytes)) + text_bytes
    @staticmethod
    def read_varint_from_bytes(data_bytes, offset=0):
        """Czyta VarInt z dowolnego obiektubytes/bytearray od wskazanego offsetu"""
        num_read = 0
        result = 0

        while True:
            if offset + num_read >= len(data_bytes):
                raise ValueError("Za mało danych na VarInt")

            read_byte = data_bytes[offset + num_read]
            value = read_byte & 0x7F
            result |= value << (7 * num_read)
            num_read += 1

            if (read_byte & 0x80) == 0:
                break

            if num_read > 5:
                raise ValueError("VarInt jest za długi!")

        return result, num_read


