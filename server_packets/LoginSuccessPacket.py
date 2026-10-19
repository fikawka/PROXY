import uuid

from Packet import Packet


class LoginSuccessPacket(Packet):
    def __init__(self, username: str):
        packet_id = b'\x02'
        super().__init__(packet_id)
        self.player_uuid = str(uuid.uuid4())
        self.username = username

    def encode(self):
        content = self.packet_id + Packet.write_string(self.player_uuid) + Packet.write_string(self.username)
        final_packet = Packet.encode_varint(len(content)) + content
        return final_packet
