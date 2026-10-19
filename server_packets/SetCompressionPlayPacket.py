import zlib

from Packet import Packet


class SetCompressionPlayPacket(Packet):  # PAKIET SERWER-KLIENT
    def __init__(self, set_compression_threshold: int, actual_compression_threshold: int = -1): # compresion_threshold = maximum packet size before compression applies
        self.packet_id = b'\x46'
        self.actual_compression_threshold = actual_compression_threshold
        super().__init__(self.packet_id)
        self.set_compression_threshold = set_compression_threshold # Jesli 0 to wszystkie pakiety, jesli na minusie to wylacza kompresje

    def encode(self):
        if self.actual_compression_threshold < 0:
            content = (
                self.packet_id
                + Packet.encode_varint(self.set_compression_threshold)
            )
            final_packet = Packet.encode_varint(len(content)) + content
            return final_packet
        elif self.actual_compression_threshold < 0:
            content = (
                Packet.encode_varint(0)
                + Packet.encode_varint(self.packet_id)
                + Packet.encode_varint(self.set_compression_threshold)
            )
            final_packet = Packet.encode_varint(len(content)) + content
            return final_packet





