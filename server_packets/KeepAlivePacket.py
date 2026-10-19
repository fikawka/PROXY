import struct

from Packet import Packet


class KeepAlivePacket(Packet):
    def __init__(self, additional_id):
        self.packet_id = b'\x00'
        super().__init__(self.packet_id)
        self.additional_id = additional_id
    def encode(self):
        content = (
            self.packet_id
            + Packet.encode_varint(self.additional_id)
        )
        final_packet = Packet.encode_varint(len(content)) + content
       # print("Enconding keep alive...", self.additional_id)
        return final_packet