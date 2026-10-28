import time

from PacketUtils import PacketUtils
from bot import Bots, BotReceivedPacketHandler

active_bots = Bots.all_active_bots
buffer = bytearray()
def receive_packets():
    while True:
        time_start = time.time()
        for i in range(len(active_bots)):
            try:
                sock = active_bots[i].socket
                buffer.extend(sock.recv(1024))
                if len(buffer) < 1:
                    continue
                try:
                    packet_length, bytes_read = PacketUtils.read_varint_from_buffer(buffer)
                except ValueError:
                    print("Value err")
                    continue
                full_packet_length = bytes_read + packet_length
                if len(buffer) < full_packet_length:
                    continue
                packet_data = buffer[:full_packet_length]
                BotReceivedPacketHandler.handle_packet(packet_data, active_bots[i])
                del buffer[:full_packet_length]

            except Exception as e:
                Bots.remove_bot(active_bots[i])

                pass

        time_end = time.time()
        time_elapsed = time_end - time_start
        if time_elapsed < 0.01:
            time.sleep(0.01 - time_elapsed)



