import queue
import threading
import time

from independent_modules import PlayerList
from server_packets.ChangeGameStatePacket import ChangeGameStatePacket
from server_packets.ChatMessagePacket import ChatMessagePacket

kolejkaDoChatu = queue.Queue()
playerlist = PlayerList.PlayerList()
def addChatMessage(player: str, message):
    if message.startswith("!"):
        kolejkaDoChatu.put(f"[Proxy]{player}: {message}")

def ChatThread():
    from independent_modules import Console
    while True:
        if kolejkaDoChatu.qsize() > 0:
            dane_wiadomosci = kolejkaDoChatu.get()
            Console.sendConsoleMessage(dane_wiadomosci)
            for player in PlayerList.playerList:
                player.easySendPacket(ChatMessagePacket(dane_wiadomosci, None, color="purple"))
        time.sleep(0.01)

chatThread = threading.Thread(target=ChatThread)
chatThread.start()





