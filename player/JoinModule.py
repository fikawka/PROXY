import socket
import threading
import time
import zlib

import CommandHandler
import UUIDGenerator

from Crasher import Crasher
from Packet import Packet
from PacketUtils import PacketUtils
from client_packets.ClientHandshakePacket import ClientHandshakePacket
from client_packets.ClientLoginStartPacket import ClientLoginStartPacket
from independent_modules.ThreadManager import ThreadManager
from player import Player
from player.JoinModuleServerDataSender import JoinModuleServerDataSender
from server_packets.ChatMessagePacket import ChatMessagePacket
from server_packets.PositionAndLookPacket import PositionAndLookPacket
from server_packets.SetCompressionPlayPacket import SetCompressionPlayPacket


class JoinModule:
    def __init__(self, player: Player.Player):
        self.compression = False
        self.compression_threshold = -1
        self.ip = None
        self.port = None
        self.external_nick = None
        self.socket = None
        self.player = player
        self.join_module_sender = JoinModuleServerDataSender()
        self.join_module_sender_thread = threading.Thread(target=self.join_module_sender.send_packet_loop)
        self.join_module_sender_thread.daemon = True
        self.crasher = Crasher()

        self.compression_buffer = bytearray()
    def connect(self):
        from independent_modules import Console

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as self.socket:
            #self.player.player_state = self.player.player_state.CONNECTED_TO_EXTERNAL_SERVER
            self.socket.connect((self.ip, self.port))
            Console.sendConsoleMessage(f"Tworzenie polaczenia z {self.ip}:{self.port} ")
            if not self.player.bungee:
                self.socket.sendall(ClientHandshakePacket(server_addr=self.ip, server_port=self.port).encode())
            else:
                self.socket.sendall(ClientHandshakePacket(server_addr=f"127.0.0.1\x00127.0.0.1\x00{UUIDGenerator.generate_uuid(ign=self.external_nick)}\x00[]", server_port=self.port).encode())
            Console.sendConsoleMessage("Wysylanie handshake...")
            self.socket.sendall(ClientLoginStartPacket(self.external_nick).encode())
            Console.sendConsoleMessage("Wysylanie login start...")
            packet_length = Packet.read_varint(self.socket)
            packet_id = Packet.read_varint(self.socket)
            Console.sendConsoleMessage(f"Otrzymano pakiet o dlugosci {packet_length} i id {packet_id}")
            if packet_id == 2:
                uuid = self.readString(self.socket)
                ign = self.readString(self.socket)
                Console.sendConsoleMessage(f"Odebrano login success! ")
                packet_length = Packet.read_varint(self.socket)
                packet_id = Packet.read_varint(self.socket)
                id = self.socket.recv(4)
                gamemode = self.socket.recv(1)
                dimension = self.socket.recv(1)
                difficulty = self.socket.recv(1)
                max_players = self.socket.recv(1)
                level_type = self.readString(self.socket)
                reduced_debug_info = self.socket.recv(1)
                print(f"Odebrano pakiet: LEN: {packet_length} ID: {packet_id} id_gracza: {id} gamemode {gamemode} dimension {dimension} difficulty {difficulty} max_players {max_players} level_type: {level_type} reduced_debug_info: {reduced_debug_info}")
                Console.sendConsoleMessage("Starting the join module sender")
                self.join_module_sender_thread = threading.Thread(target=self.join_module_sender.send_packet_loop, args=(self.player, self.socket))
                self.join_module_sender_thread.start()
                self.player.join_module_data_downloader.downloadData(socket=self.socket, player=self.player)

            elif packet_id == 3:
                self.player.external_compression = Packet.read_varint(self.socket) # Z kompresją
                Console.sendConsoleMessage("JOIN: Kompresja wlaczona")
                self.compression = True
                #self.compression_threshold = Packet.read_varint(self.socket)
                #self.player.setExternalCompression(self.compression_threshold)
                Console.sendConsoleMessage(f"Setting compression !!!! {self.player.external_compression}")
                packet_length = Packet.read_varint(self.socket) # length of data length + compressed length of (packet id +  data)
                data_length = Packet.read_varint(self.socket) # length of uncompressed Packet ID + data
                Console.sendConsoleMessage(f"LOGIN SUCCESS Z KOMPRESJA: PACKET_LENGTH = {packet_length}, data_length = {data_length}")
                if data_length == 0:
                    packet_id = Packet.read_varint(self.socket)
                    uuid = self.readString(self.socket)
                    nick = self.readString(self.socket)
                    Console.sendConsoleMessage(f"UUID: {uuid} IGN: {nick}")
                    packet_length = Packet.read_varint(self.socket)
                    data_length = Packet.read_varint(self.socket)
                    Console.sendConsoleMessage(f"Packet_length {packet_length}, data_length {data_length}")
                    if data_length == 0:
                        packet_id = Packet.read_varint(self.socket)
                        id = self.socket.recv(4)
                        gamemode = self.socket.recv(1)
                        dimension = self.socket.recv(1)
                        difficulty = self.socket.recv(1)
                        max_players = self.socket.recv(1)
                        level_type = self.readString(self.socket)
                        reduced_debug_info = self.socket.recv(1)
                        Console.sendConsoleMessage(f"Odebrano pakiet: ID: {packet_id} id_gracza: {id} gamemode {gamemode} dimension {dimension} difficulty {difficulty} max_players {max_players} level_type: {level_type} reduced_debug_info: {reduced_debug_info}")
                        self.player.player_state = self.player.player_state.CONNECTED_TO_EXTERNAL_SERVER
                        self.join_module_sender_thread = threading.Thread(target=self.join_module_sender.send_packet_loop, args=(self.player, self.socket))
                        self.join_module_sender_thread.start()
                        self.player.join_module_data_downloader.downloadData(socket=self.socket, player=self.player)
                    elif data_length > 0:
                        rest = self.socket.recv(205)
                        rest_decompressed = zlib.decompress(rest)
                        Console.sendConsoleMessage(rest_decompressed)
                        Console.sendConsoleMessage(f"Packet id:  {PacketUtils.read_varint_from_bytes(rest_decompressed)}")
                        #time.sleep(0.3)
                        self.player.player_state = self.player.player_state.CONNECTED_TO_EXTERNAL_SERVER
                        self.join_module_sender_thread = threading.Thread(target=self.join_module_sender.send_packet_loop, args=(self.player, self.socket))
                        self.join_module_sender_thread.start()
                        self.player.join_module_data_downloader.downloadData(socket=self.socket, player=self.player)








    def readString(self, sock: socket.socket):
        string_length = Packet.read_varint(sock)
        server_address = self.socket.recv(string_length).decode("utf-8")
        return server_address
    def quit(self):
        self.player.sendPacket(PositionAndLookPacket(x=30000, y=50, z=6000, yaw=0, pitch=15, flags=0))
        self.socket.close()
        self.player.player_state = self.player.player_states.CONNECTED_TO_PROXY_LOBBY
        ThreadManager.stop_thread(self.join_module_sender_thread)







