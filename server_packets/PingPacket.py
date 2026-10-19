import json

from Packet import Packet


class PingPacket(Packet):


    def __init__(self, motd_path: str):
        self.motd = json.load(open(motd_path))
        packet_id = b'\x00'
        super().__init__(packet_id)

    def encode(self):

        json_data = json.dumps(self.motd).encode("utf-8")
        packet_content = b'\x00' + super().encode_varint(len(json_data)) + json_data
        final_packet = super().encode_varint(len(packet_content)) + packet_content
        return final_packet

