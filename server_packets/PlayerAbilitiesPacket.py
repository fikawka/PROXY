import struct

from Packet import Packet


class PlayerAbilitiesPacket(Packet):
    def __init__(self, flags, flying_speed: float, fov_modifier: float):
        packet_id = b'\x3F'
        super().__init__(packet_id)
        self.flags = flags
        self.flying_speed = flying_speed
        self.fov_modifier = fov_modifier
    def encode(self):
        content = (
            self.packet_id
            + struct.pack(">B", self.flags)
            + struct.pack(">f", self.flying_speed)
            + struct.pack(">f", self.fov_modifier)
        )
        final_packet = Packet.encode_varint(len(content)) + content
        return final_packet

