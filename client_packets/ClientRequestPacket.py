from Packet import Packet


class ClientRequestPacket(Packet):
    def __init__(self):
        super().__init__(packet_id=b'\x00')

    def encode(self):
        content = (self.packet_id)
        final_packet = Packet.encode_varint(len(self.packet_id)) + content
        return final_packet