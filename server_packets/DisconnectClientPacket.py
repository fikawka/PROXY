import struct

from Packet import Packet
import json

class DisconnectClientPacket(Packet):
    def __init__(self, reason):
        self.reason = reason
        self.packet_id = b'\x40'
        super().__init__(self.packet_id)
    def encode(self):
        data = {
            "text": self.reason
        }
        json_reason = json.dumps(data).encode("utf-8")
        packet_content = self.packet_id + super().encode_varint(len(json_reason)) + json_reason
        final_packet = super().encode_varint(len(packet_content)) + packet_content
        return final_packet
        print("Wysyl")
        return final_packet





