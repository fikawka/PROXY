import socket
import json

#from bot.BotProcess import startBotProcess
from independent_modules.ProxyChecker import ProxyChecker
from player.Player import Player
from independent_modules import PlayerList
from independent_modules.ThreadManager import ThreadManager

port = 25565
host = "127.0.0.1"
gamemode = 0
x = 0
y = 64
z = 0


motd = json.load(open("config/motd.json"))

def start_server():
    threadManager = ThreadManager()
    threadManager.start()
   # proxychecker = ProxyChecker()
    listagraczy = PlayerList.PlayerList()
    listagraczy.start()
    playerlist = PlayerList
    with socket.socket( socket.AF_INET, socket.SOCK_STREAM ) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
        s.bind((host, port))
        s.listen(5)
        s.settimeout(None)



        try:
            while True:
                conn, addr = s.accept()
                print("Otrzymano połaczenie")
                player = Player(conn, addr, None)
        except KeyboardInterrupt:
            print("Zatrzymywanie serwera..")
        finally:
            s.close()


print("Minecraft proxy 1.0 - Organiczne w pythonie")
# Narazie tworze tylko serwer jakis basic, potem thready itp - potem joina i boty stworzyc, ewentualnie jakis crasher jesli jeszcze sie da
if __name__ == "__main__":
    start_server()
    startBotProcess()








