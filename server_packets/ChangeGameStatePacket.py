import struct

from Packet import Packet


class ChangeGameStatePacket(Packet, ):
    def __init__(self, reason: int, value: float):
        self.packet_id = b'\x2B'
        self.reason = reason
        self.value = value
        super().__init__(self.packet_id)
    def encode(self):
        content = (
            self.packet_id
            + struct.pack(">B", self.reason)
            + struct.pack(">f", self.value)

        )
        final_packet = Packet.encode_varint(len(content)) + content
        return final_packet
