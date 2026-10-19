import struct

from Packet import Packet


class JoinGamePacket(Packet):
    def __init__(self, entity_id: int, gamemode: int, dimension: int, difficulty: int, max_players: int, level_type: str):
        packet_id = b'\x01'
        super().__init__(packet_id)
        self.entity_id = entity_id
        self.gamemode = gamemode
        self.dimension = dimension
        self.difficulty = difficulty
        self.max_players = max_players
        self.level_type = level_type

    def encode(self):
        content = (
            b'\x01'
            + struct.pack(">i", self.entity_id)
            + struct.pack(">B", self.gamemode)
            + struct.pack(">B", self.dimension)
            + struct.pack(">B", self.difficulty)
            + struct.pack(">B", self.max_players)
            + self.write_string(self.level_type)
            + struct.pack(">B", 0) ## Reduced debug info na FALSE
        )
        final_packet = Packet.encode_varint(len(content)) + content
        return final_packet