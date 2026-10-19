import struct

from Packet import Packet


class PositionAndLookPacket(Packet):
    def __init__(self, x: float, y: float, z: float, yaw: float, pitch: float, flags):
        packet_id = b'\x08'
        super().__init__(packet_id)
        self.x = x
        self.y = y
        self.z = z
        self.yaw = yaw
        self.pitch = pitch
        self.flags = flags
    def encode(self):
        content = (
            self.packet_id
            + struct.pack(">d", self.x)
            + struct.pack(">d", self.y)
            + struct.pack(">d", self.z)
            + struct.pack(">f", self.yaw)
            + struct.pack(">f", self.pitch)
            + struct.pack(">B", self.flags)
        )
        final_packet = Packet.encode_varint(len(content)) + content
        return final_packet
