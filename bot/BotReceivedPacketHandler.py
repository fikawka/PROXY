from PacketUtils import PacketUtils
from bot import BotsDataSender
from player import PacketTranslator


def handle_packet(data, bot):
    length_packet, bytes_read = PacketUtils.read_varint_from_bytes(data) ## Rewrite by sie przydal ale trudno spaghetti
    if bot.bot_state == bot.bot_states.LOGIN:
        if bot.compression_level is None:
            packet_id, bytes_read1 = PacketUtils.read_varint_from_bytes(data, bytes_read)
            bytes_read_total = bytes_read + bytes_read1
            if packet_id == 3:
                compression_level = PacketUtils.read_varint_from_bytes(data, bytes_read_total)
                bot.compression_level = compression_level
            elif packet_id == 2:
                bot.bot_state = bot.bot_states.PLAY
        else:
            data_decompressed = PacketTranslator.translate_packet_from_compressed_to_decompressed(data)
            length_packet, bytes_read = PacketUtils.read_varint_from_bytes(data_decompressed)
            packet_id, bytes_read1 = PacketUtils.read_varint_from_bytes(data_decompressed, bytes_read)
            if packet_id == 2:
                bot.bot_state = bot.bot_states.PLAY

    if bot.bot_state == bot.bot_states.PLAY:
        if bot.compression_level is None:
            packet_id, bytes_read1 = PacketUtils.read_varint_from_bytes(data, bytes_read)
            if packet_id == 0:
                BotsDataSender.send_packet(data,bot) ## odsylam pakiet keep alive
                
        elif bot.compression_level >= 0:
            data_decompressed = PacketTranslator.translate_packet_from_compressed_to_decompressed(data)
            length_packet, bytes_read = PacketUtils.read_varint_from_bytes(data_decompressed)
            packet_id = PacketUtils.read_varint_from_bytes(data_decompressed, bytes_read)
            if packet_id == 0:
                BotsDataSender.send_packet(data,bot) ## odsylam pakiet keep alive
                pass # odsylamy keep alive




