# Zajmuje sie pobieraniem od serwera danych
from PacketUtils import PacketUtils
from independent_modules import Console
from player import PacketChecker, PacketTranslator


class JoinModuleServerDataDownloader:
    def __init__(self):
        self.buffer = bytearray()

    def downloadData(self, socket, player):
        while player.player_state == player.player_states.CONNECTED_TO_EXTERNAL_SERVER:
            try:
                data = socket.recv(4096)
                self.buffer.extend(data)
                while True:
                    if len(self.buffer) < 1:
                        break
                    try:
                        packet_length, bytes_read = PacketUtils.read_varint_from_buffer(self.buffer)
                    except ValueError as e:
                        Console.sendConsoleMessage(f"Error: {e}")
                    total_packet_size = bytes_read + packet_length
                    if len(self.buffer) < total_packet_size:
                        break
                    packet_data = self.buffer[:total_packet_size]
                    del self.buffer[:total_packet_size]
                    if player.external_compression < 0:
                        PacketChecker.check_and_pass_incoming(player=player, packet_data=packet_data)
                    elif player.external_compression >= 0:
                        uncompressed_packet = PacketTranslator.translate_packet_from_compressed_to_decompressed(packet_data=packet_data)
                        PacketChecker.check_and_pass_incoming(player=player, packet_data=uncompressed_packet)
            except Exception as e:
                Console.sendConsoleMessage(f"Error: {e}")
                player.joiner.quit()

                break



