from PacketUtils import PacketUtils


class PlayerDataReceiverLoop:
    def __init__(self, player):
        self.player = player
        self.buffer = bytearray()

    def receiver_loop(self):  # Pobiera pakiety od uzytkownika
        while self.player.isconnected:
            try:
                data = self.player.client_socket.recv(4096)
                self.buffer.extend(data)
            except Exception as e:
                print(e)
                break
            while True: # Trzeba to zmienic
                if len(self.buffer) < 1:
                    break
                try:
                    packet_length, varint_bytes_count = PacketUtils.read_varint_from_buffer(self.buffer)
                except ValueError:
                    break
                total_packet_size = varint_bytes_count + packet_length
                if len(self.buffer) < total_packet_size:
                    break
                raw_packet_data = self.buffer[:total_packet_size]
                self.player.packet_queue.put(raw_packet_data)
                del self.buffer[:total_packet_size]



