from Packet import Packet


class ClientLoginStartPacket(Packet):
    def __init__(self, name):
        self.packet_id = b'\x00'
        super().__init__(self.packet_id)
        self.name = name
    def encode(self):
        content = (
            self.packet_id
            + Packet.write_string(self.name)

        )
        final_packet = Packet.encode_varint(len(content)) + content
        return final_packet
