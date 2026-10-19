import queue
import threading
import time
import player.PlayerUtils
from server_packets.DisconnectClientPacket import DisconnectClientPacket
from player import Player
from independent_modules import Console

playerList = []
nameList = []
addPlayerQueue = queue.Queue()
removePlayerQueue = queue.Queue()

class PlayerList(threading.Thread):
    _instancja = None
    def __new__(cls):
        if cls._instancja is None:
            Console.sendConsoleMessage("Creating object of Playerlist...")
            cls._instancja = super().__new__(cls)
        return cls._instancja

    def run(self):
        while True:
            while addPlayerQueue.qsize() > 0:
                p = addPlayerQueue.get()
                playerList.append(p)
                if p.getName() == None:
                    print(f"Error name not found, {p.getName()} i {p.name}")
                nameList.append(p.getName())
                Console.kolejkaDoKonsoli.put(f"PLAYER: {p.getName()} joined")


            while removePlayerQueue.qsize() > 0:
                p = removePlayerQueue.get()
                try:
                    nameList.remove(p.name)
                except Exception as e:
                    Console.sendConsoleMessage(f"Error while removing player {e} (name)")
                try:
                    playerList.remove(p)
                except Exception as e:
                    print(f"ERROR WHILE REMOVING PLAYER: {e} (player)")
                print(f"PLAYER: {p.getName()} removed from playerlist!")

            time.sleep(0.001)



    def addPlayer(self, player: Player.Player):
        addPlayerQueue.put(player)
        Console.sendConsoleMessage(f"PLAYER: {player.getName()} added to playerlist!")

    def getAllNames(self):
        return nameList
    def doesPlayerExist(self, playerName):
        if playerName in nameList:
            return True
        else:
            return False

    def removePlayer(self, playerName: str):
        p = self.getPlayerWithName(playerName)

        if p == None:
            Console.sendConsoleMessage(f"PLAYER: {playerName} not found while removing")
        else:
            removePlayerQueue.put(p)



    def kickPlayer(self, playerName: str, reason: str):
        print(f"KICK PLAYER CALLED: {playerName} i {reason}")
        if self.doesPlayerExist(playerName):
            for player in playerList:
                if player.getName() == playerName:
                    player.sendPacket(DisconnectClientPacket(reason))
                    playerList.remove(player)
                    nameList.remove(playerName)
                    Console.kolejkaDoKonsoli.put(f"REMOVED PLAYER: {playerName} ", )
                    break
        else:
            Console.kolejkaDoKonsoli.put(f"Player of name {playerName} not found")
    def getPlayerWithName(self, playerName):
        if playerName in nameList:
            for player in playerList:
                if player.getName() == playerName:
                    print(f"Player found, {player}")
                    return player

        else:
            print("Function failed")
            print(f"Dlugosc Player {len(playerList)}")
            return None


