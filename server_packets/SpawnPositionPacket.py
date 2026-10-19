import struct

from Packet import Packet


class SpawnPositionPacket(Packet):
    def __init__(self, x,y,z):
        self.packet_id = b'\x05'
        self.x = x
        self.y = y
        self.z = z
        super().__init__(self.packet_id)

    def encode(self):
        encoded_position = ((self.x & 0x3FFFFFF) << 38) | ((self.y & 0xFFF) << 26) | (self.z & 0x3FFFFFF)
        content = (
                self.packet_id + struct.pack(">q", encoded_position)
        )
        final_packet = Packet.encode_varint(len(content)) + content
        return final_packet
