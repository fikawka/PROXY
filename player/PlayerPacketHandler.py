import CommandHandler
import PacketUtils
from independent_modules import Console, ProxyChat


class PlayerPacketHandler:
    def __init__(self, player):
        self.player = player
    def handle_packet(self, packet_data):
        total_bytes_read = 0
        if len(packet_data) < 1:
            return
        try:
            packet_length, bytes_read = PacketUtils.PacketUtils.read_varint_from_bytes(packet_data)
            total_bytes_read += bytes_read
            packet_id, bytes_read2 = PacketUtils.PacketUtils.read_varint_from_bytes(packet_data, total_bytes_read)
            total_bytes_read += bytes_read2
            if packet_id == 0x01:
                string_length, bytes_read = PacketUtils.PacketUtils.read_varint_from_bytes(packet_data, bytes_read)
                total_bytes_read += bytes_read
                mess = packet_data[total_bytes_read:len(packet_data)].decode("utf-8")
                print(mess)
                if mess.startswith(","):
                    CommandHandler.handleCommand(gracz=self.player, command=mess)
                if mess.startswith("!"):
                    ProxyChat.addChatMessage(player=self.player, message=mess)

        except ConnectionAbortedError or UnicodeDecodeError as e:
            self.player.disconnect()
