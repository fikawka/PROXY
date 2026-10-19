import struct

from Packet import Packet


class ClientSettingsPacket(Packet):
    def __init__(self,view_distance, ):
        self.packet_id = b'\x15'
        self.locale = "en_GB"
        self.view_distance = view_distance
        self.chat_mode = 0
        self.chat_colors = b'\x01'
        self.display_skin_parts = b'\x7F'
        super().__init__(self.packet_id)
    def encode(self):
        content = (
            self.packet_id
            + Packet.write_string("en_GB")
            + struct.pack(">B", self.view_distance)
            + struct.pack(">B", self.chat_mode) # chat mode
            + struct.pack(">B", 1) # chat colors
            + self.display_skin_parts # skin parts

        )
        final_packet = Packet.encode_varint(len(content)) + content
        return final_packet
