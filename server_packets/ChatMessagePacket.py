import struct
import zlib

from Packet import Packet
import json

class ChatMessagePacket(Packet):
    def __init__(self, message, sender, bold="false", color="", compression_threshold=-1):
        self.packet_id = b'\x02'
        super().__init__(self.packet_id)
        self.message = message
        self.sender = sender
        self.bold = bold
        self.color = color
        self.compression_threshold = compression_threshold
    def encode(self):
        if self.compression_threshold < 0:
            dict = {
                "text": self.message,
                "bold": self.bold,
                "color": self.color
            }
            json_bytes = Packet.write_chat_component(dict)
            content = (
                self.packet_id
                + Packet.encode_varint(len(json_bytes))
                + json_bytes
                + struct.pack(">b", 0)
            )
            final_packet = Packet.encode_varint(len(content)) + content
            return final_packet
        elif self.compression_threshold > 0:
            dict = {
                "text": self.message,
                "bold": self.bold,
                "color": self.color
            }
            json_bytes = Packet.write_chat_component(dict)
            content_uncompressed = (
                self.packet_id
                + Packet.encode_varint(len(json_bytes))
                + json_bytes
                + struct.pack(">b", 0)
            )
            if len(content_uncompressed) < self.compression_threshold:
                packet_with_data_length = Packet.encode_varint(0) + content_uncompressed
                final_packet = Packet.encode_varint(len(packet_with_data_length)) + packet_with_data_length
                return final_packet
            else:
                content_compressed = zlib.compress(content_uncompressed, level=6)
                packet_with_data_length = Packet.encode_varint(len(content_uncompressed)) + content_compressed
                final_packet = Packet.encode_varint(len(packet_with_data_length)) + packet_with_data_length
                return final_packet




