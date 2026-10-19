import zlib

from Packet import Packet
from PacketUtils import PacketUtils


def translate_packet_from_compressed_to_decompressed(packet_data):
    bytes_read_total = 0
    packet_length, bytes_read = PacketUtils.read_varint_from_bytes(packet_data)
    total_packet_length = packet_length + bytes_read
    bytes_read_total += bytes_read
    data_length, bytes_read1 = PacketUtils.read_varint_from_bytes(packet_data, offset=bytes_read_total)
    bytes_read_total += bytes_read1
    if data_length == 0:
        packet = packet_data[bytes_read_total:total_packet_length]
        final_packet = Packet.encode_varint(len(packet)) + packet
        return final_packet
    elif data_length > 0:
        packet_data_compressed = packet_data[bytes_read_total:total_packet_length]
        packet_data_decompressed = zlib.decompress(packet_data_compressed)
        final_packet = Packet.encode_varint(len(packet_data_decompressed)) + packet_data_decompressed
        return final_packet


def translate_packet_from_decompressed_to_compressed(packet_data, compression_threeshold):
    bytes_read_total = 0
    packet_length, bytes_read = PacketUtils.read_varint_from_bytes(packet_data)
    total_packet_length = packet_length + bytes_read
    bytes_read_total += bytes_read
    packet_data_decompressed = packet_data[bytes_read:]
    packet_id, bytes_read1 = PacketUtils.read_varint_from_bytes(packet_data_decompressed)
    length_packet_data_decompressed = len(packet_data_decompressed)
    if length_packet_data_decompressed < compression_threeshold:
        packet = Packet.encode_varint(0) + packet_data_decompressed
        final_packet = Packet.encode_varint(len(packet)) + packet
        #print(f"length: {len(final_packet)} packet_id : {packet_id} hex: {final_packet.hex()}")
        return final_packet
    elif length_packet_data_decompressed >= compression_threeshold:
        packet_data_compressed = zlib.compress(packet_data_decompressed, level=6)
        packet = Packet.encode_varint(length_packet_data_decompressed) + packet_data_compressed
        final_packet = Packet.encode_varint(len(packet)) + packet
        print("!")
        return final_packet






