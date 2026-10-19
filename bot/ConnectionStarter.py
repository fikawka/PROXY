import multiprocessing
import socket
import time

from bot import BotsDataReceiver, Bots
from bot.Bot import Bot,
from client_packets.ClientHandshakePacket import ClientHandshakePacket
from client_packets.ClientLoginStartPacket import ClientLoginStartPacket

do_wystartowania = multiprocessing.Queue()
def connection_starter():
    while True:
        ign_number = 0
        czas_teraz = time.time()
        if do_wystartowania.qsize() > 0:
            data = do_wystartowania.get()
            ip = data[0]["ip"]
            port = data[0]["port"]
            nick = data[0]["nick"]
            amount = data[0]["amount"]
            owner = data[1]
            for i in range(amount):
                try:
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    s.connect((ip, port))
                    s.sendall(ClientHandshakePacket(server_addr=ip, server_port=port).encode())
                    s.sendall(ClientLoginStartPacket(name=f"{nick}{ign_number}").encode())
                    bot_obj = Bot(owner=owner, socket=s, nick=f"{nick}{ign_number}")
                    bot_obj.bot_state = bot_obj.bot_states.LOGIN
                    ign_number += 1
                    Bots.add_active_bot(bot_obj)


                except Exception as e:
                    print(f"Error while connecting bots {e}")



        czas_koniec = time.time()
        time_elapsed = czas_teraz - czas_koniec
        if time_elapsed < 0.01:
            time.sleep(0.01 - time_elapsed)
def startConnection(data: dict, owner):
    data_and_owner_tuple = (data, owner)
    do_wystartowania.put(data)


