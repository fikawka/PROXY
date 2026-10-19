import CommandHandler
from PacketUtils import PacketUtils
from independent_modules import ProxyChat, Console
from player import PacketTranslator
from server_packets.ChatMessagePacket import ChatMessagePacket


def check_and_pass_incoming (player, packet_data,): # UWAGA PRZESYLASZ TUTAJ JUZ ALBO ZDEKOMPRESOWANY PAKIET, ALBO PRZETLUMACZONY NA DECOMPRESSED!!!
    total_bytes_read = 0
    packet_length, bytes_read = PacketUtils.read_varint_from_bytes(packet_data)
    total_packet_length = packet_length + bytes_read
    total_bytes_read += bytes_read
    packet_id, bytes_read = PacketUtils.read_varint_from_bytes(packet_data, bytes_read)
    total_bytes_read += bytes_read
    if packet_id == 64:
        player.joiner.quit()
        text = packet_data[total_bytes_read: total_packet_length].decode("utf-8")
        print("got it")
        player.sendPacket(ChatMessagePacket(sender=None, message="You have been kicked for: " + text))
        return
    elif packet_id == 1:
        return
    player.do_wyslania_queue.put(packet_data)

global buggy_packet
buggy_packet = 0
def check_and_pass_outgoing (player, packet_data,):

    #print("RAW CLIENT PACKET:", packet_data.hex())
   # print(len(packet_data))
    total_bytes_read = 0
    packet_length, bytes_read = PacketUtils.read_varint_from_bytes(packet_data)
    total_packet_length = packet_length + bytes_read
    total_bytes_read += bytes_read
    packet_id, bytes_read1 = PacketUtils.read_varint_from_bytes(packet_data, total_bytes_read)
    total_bytes_read += bytes_read1
    if packet_id == 1:
        string_length, bytes_read2 = PacketUtils.read_varint_from_bytes(packet_data, total_bytes_read)
        total_bytes_read += bytes_read2
        message = packet_data[total_bytes_read: total_packet_length].decode("utf-8")
        if message.startswith(","):
            CommandHandler.handleCommand(player, message)
            return
        elif message.startswith("!"):
            ProxyChat.addChatMessage(player.getName(), message)
            return
    if player.external_compression >= 0:
        compressed_packet = PacketTranslator.translate_packet_from_decompressed_to_compressed(packet_data=packet_data, compression_threeshold=player.external_compression)
        player.joiner.join_module_sender.to_server_send_queue.put(compressed_packet)
        #print(compressed_packet.hex())
    else:
        player.joiner.join_module_sender.to_server_send_queue.put(packet_data)
    #print(f"wysylam pakiet o dlugosci {packet_length} i id {packet_id}")



