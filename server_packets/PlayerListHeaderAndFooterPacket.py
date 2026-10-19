from Packet import Packet
import json

class PlayerListHeaderAndFooterPacket(Packet):
    def __init__(self, header: str, footer: str, color:str):
        self.packet_id = b'\x47'
        super().__init__(self.packet_id)
        self.header = header
        self.footer = footer
        self.color = color
    def encode(self):
        glowa = {
            "text": self.header,
            "bold": "true",
            "color": self.color
        }
        stopa = {
            "text": self.footer,
            "bold": "true",
            "color": self.color
        }
        json_bytes_glowa = Packet.write_chat_component(glowa)
        json_bytes_footer = Packet.write_chat_component(stopa)
        content = (
            self.packet_id
            + Packet.encode_varint(len(json_bytes_glowa))
            + json_bytes_glowa
            + Packet.encode_varint(len(json_bytes_footer))
            + json_bytes_footer

        )
        final_packet = Packet.encode_varint(len(content)) + content
        return final_packet


