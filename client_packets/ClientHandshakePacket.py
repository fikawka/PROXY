import struct

from Packet import Packet


class ClientHandshakePacket(Packet):
    def __init__(self, server_addr:str, server_port, protocol_version=47, next_state=2):
        self.packet_id = b'\x00'
        super().__init__(self.packet_id)
        self.protocol_version = protocol_version
        self.server_addr = server_addr
        self.server_port = server_port
        self.next_state = next_state
    def encode(self):
        content = (
            self.packet_id + Packet.encode_varint(self.protocol_version)
            + Packet.write_string(self.server_addr)
            + struct.pack(">H", self.server_port)
            + Packet.encode_varint(self.next_state)
        )
        final_packet = Packet.encode_varint(len(content)) + content
        from independent_modules import Console
        Console.sendConsoleMessage(f"Wysylanie handshake do {self.server_addr} {self.server_port}")
        return final_packet

