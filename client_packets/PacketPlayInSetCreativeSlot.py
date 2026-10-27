import struct

from Packet import Packet


class PacketPlayInSetCreativeSlot(Packet):
    def __init__(self, slot_nr, item_id, item_count, item_damage, nbt_data):
        self.packet_id = b'\x10'
        self.slot_nr = slot_nr
        self.item_id = item_id
        self.item_count = item_count
        self.item_damage = item_damage
        self.nbt_data = nbt_data
        super().__init__(self.packet_id)
    def encode(self):
        data = (
                            self.packet_id
                           + struct.pack(">h", self.slot_nr)
                           +struct.pack(">h", self.item_id)
                            +struct.pack(">b", self.item_count)
                           +struct.pack(">h", self.item_damage)
                           +self.nbt_data
        )
        final_packet = Packet.encode_varint(len(data)) + data
        print(len(data))
        return final_packet