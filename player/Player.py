import threading
import time
from enum import Enum
from queue import Queue
from random import Random

from player.GameLogic import GameLogic
from player.JoinModule import JoinModule
from player.JoinModuleServerDataDownloader import JoinModuleServerDataDownloader
from player.JoinModuleServerDataSender import JoinModuleServerDataSender
from player.PlayerDataReceiverLoop import PlayerDataReceiverLoop
from player.PlayerDataSenderLoop import PlayerDataSenderLoop
from player.PlayerPacketHandler import PlayerPacketHandler
from server_packets.ChatMessagePacket import ChatMessagePacket
from server_packets.DisconnectClientPacket import DisconnectClientPacket
from server_packets.JoinGamePacket import JoinGamePacket
from server_packets.KeepAlivePacket import KeepAlivePacket
from server_packets.LoginDisconnectPacket import LoginDisconnectPacket
from server_packets.LoginSuccessPacket import LoginSuccessPacket
from Packet import Packet
from server_packets.PingPacket import PingPacket
from server_packets.PlayerAbilitiesPacket import PlayerAbilitiesPacket
from independent_modules import PlayerList
from server_packets.PlayerListHeaderAndFooterPacket import PlayerListHeaderAndFooterPacket
from server_packets.PositionAndLookPacket import PositionAndLookPacket
from server_packets.SetCompressionPlayPacket import SetCompressionPlayPacket
from server_packets.SpawnPositionPacket import SpawnPositionPacket
from independent_modules.ThreadManager import ThreadManager


class Player:
    def __init__(self, client_socket, adress, name):
        self.client_socket = client_socket
        self.player_data_receiver_loop = PlayerDataReceiverLoop(self)
        self.player_packet_handler = PlayerPacketHandler(player=self)
        self.player_data_sender_loop = PlayerDataSenderLoop(self)
        self.gamelogic = GameLogic(player=self)
        self.external_socket = None
        self.adress = adress
        self.isconnected = True
        self.receiver_thread = threading.Thread(target=self.start_connection)
        self.receiver_thread.daemon = True
        self.sender_thread = threading.Thread(target=self.player_data_sender_loop.tick_loop)
        self.sender_thread.daemon = True
        self.packet_queue = Queue()
        self.buffer = bytearray()
        self.external_buffer = bytearray()
        ThreadManager.addThread(self.receiver_thread)
        self.tick_counter = 0
        self.name = None
        self.connected_to_external = False
        self.external_name = None
        self.playerlist = PlayerList.PlayerList()
        self.packet_from_external_queue = Queue()
        self.raw_packet_queue = Queue()
        self.do_wyslania_queue = Queue()
        self.external_compression = -1
        self.joiner = JoinModule(self)
        self.player_state = PlayerState.CONNECTED_TO_PROXY_LOBBY
        self.join_module_data_downloader = JoinModuleServerDataDownloader()
        self.player_states = PlayerState
        self.bungee = False



        # Watek do odbierania pakietow przez serwer otrzymanych od gracza (Ciągle bez ticków)
        # Wątek służacy do wysyłania pakietów przez serwer do gracza (20tps - co 0.05s)

    def create_join_thread(self):
        join_thread = threading.Thread(target=self.joiner.connect)
        join_thread.daemon = True
        return join_thread

    def extend_external_buffer(self, data):
        self.external_buffer.extend(data)
    def join_server(self, ip, port, ign_on_server):
        self.joiner.ip = ip
        self.joiner.port = port
        self.joiner.external_nick = ign_on_server
        watek = self.create_join_thread()
        watek.start()


    def start_connection(self): # connect
        try: # tutaj bedzie handshake
            packet_length = Packet.read_varint(self.client_socket)
            packet_id = Packet.read_varint(self.client_socket)
            print(packet_id)
            if packet_id == 0: # handshake received
                protocol_version = Packet.read_varint(self.client_socket)
                addr_len = Packet.read_varint(self.client_socket)
                server_address = self.client_socket.recv(addr_len).decode("utf-8")
                server_port = int.from_bytes(self.client_socket.recv(2), "big")
                next_state = Packet.read_varint(self.client_socket)
                if next_state == 1:
                    packet_length = Packet.read_varint(self.client_socket)
                    packet_id = Packet.read_varint(self.client_socket)
                    #print(f"Odebrano kolejny pakiet, dlugosc: {packet_length} i ID {packet_id}")
                    ping = PingPacket("config/motd.json")
                    self.client_socket.sendall(ping.encode())
                    self.disconnect_login()
                elif next_state == 2:
                    # obsluga loginstart pakietu
                    packet_length = Packet.read_varint(self.client_socket)
                    packet_id = Packet.read_varint(self.client_socket)
                    user_length = Packet.read_varint(self.client_socket)
                    self.name = self.client_socket.recv(user_length).decode("utf-8")

                    print(F"Packet Received: ID: {packet_id}, length: {packet_length}, username: {self.name} ")
                    import independent_modules.PlayerList
                    if self.name in PlayerList.nameList:
                        from independent_modules import Console
                        Console.sendConsoleMessage(f"Player {self.name} tried to connect however he is already connected")
                        self.easySendPacket(LoginDisconnectPacket("You are already connected to this server!"))
                        #time.sleep(0.001)
                        self.disconnect_login()

                    else:
                        if packet_id == 0:
                            self.client_socket.sendall(LoginSuccessPacket(self.name).encode())
                            self.client_socket.sendall(
                                JoinGamePacket(entity_id=1, gamemode=0, dimension=0, difficulty=0, max_players=100,
                                            level_type="flat").encode())
                            self.client_socket.sendall(SpawnPositionPacket(0,64,0).encode())
                            self.client_socket.sendall(PlayerAbilitiesPacket(flags=0, flying_speed=0.05, fov_modifier=0.1).encode())
                            self.client_socket.sendall(PositionAndLookPacket(x=0, y=64, z=0, yaw=0, pitch=0, flags=0).encode())
                            self.playerlist.addPlayer(self)
                            ThreadManager.addThread(self.sender_thread)
                            self.client_socket.sendall(
                            ChatMessagePacket(sender="", message="Witamy na proxy!", bold="true").encode())
                            self.client_socket.sendall(
                                ChatMessagePacket(sender="", message="Aby zobaczyc dostepne komendy wpisz ,help", bold="true").encode())
                            self.sendPacket(PlayerListHeaderAndFooterPacket(header="Witamy na proxy", footer="", color="green"))
                            self.player_data_receiver_loop.receiver_loop()

        except Exception as e:
            print("No wyjebalo bład")
            print(e)
            self.disconnect()



       # finally:
            #self.client_socket.close()



    def disconnect(self):
        self.isconnected = False
        self.client_socket.close()
        self.playerlist.removePlayer(self.name)
        ThreadManager.disconnectPlayerThread(self.sender_thread)
        ThreadManager.disconnectPlayerThread(self.receiver_thread)

    def disconnect_login(self):
        self.isconnected = False
        self.client_socket.close()
        ThreadManager.disconnectPlayerThread(self.sender_thread)
        ThreadManager.disconnectPlayerThread(self.receiver_thread)
    def easySendPacket(self, packet: Packet): # Wysyła pakiet odrazu, omija kolejke oraz TPS
        try:
            self.client_socket.sendall(packet.encode())
        except ConnectionAbortedError or ConnectionResetError as e:
            print(e)
            self.disconnect()
    def setisConnected(self, is_connected: bool):
        self.isconnected = is_connected
    def sendPacket(self, packet: Packet):
        self.do_wyslania_queue.put(packet.encode())

    def getName(player: Player):
        return player.name

    def read_varint_from_bytes(self, data_bytes, offset=0):
        num_read = 0
        result = 0

        while True:
            if offset + num_read >= len(data_bytes):
                raise ValueError("Za mało danych na VarInt")

            read_byte = data_bytes[offset + num_read]
            value = read_byte & 0x7F
            result |= value << (7 * num_read)
            num_read += 1

            if (read_byte & 0x80) == 0:
                break

            if num_read > 5:
                raise ValueError("VarInt jest za długi!")

        return result, num_read
class PlayerState(Enum):
    DISCONNECTED = 0
    CONNECTED_TO_PROXY_LOBBY = 1
    CONNECTED_TO_EXTERNAL_SERVER = 2



