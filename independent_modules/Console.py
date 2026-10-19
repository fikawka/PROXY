import threading
import time
import queue

import independent_modules.PlayerList as PlayerList

kolejkaDoKonsoli = queue.Queue()
def consoleInput():
    print("CONSOLE INPUT INITIALIZED")
    while True:
        user_input = str(input())
        if user_input.startswith("kick"):
            name = user_input.split(" ")[1]
            print(f"SPLIT NR0: {user_input.split(" ")[0]} nr1: {user_input.split(" ")[1]} nr2: {user_input.split(" ")[2]}")

            reason = user_input.split(" ")[2]
            PlayerList.kickPlayer(name, reason)
        elif user_input.startswith("help"):
            print("List of available console commands:")
            print("help -- Shows this help menu")
            print("kick (name) (reason) -- Kicks a player")


def consoleOutput():
    while True:
        if kolejkaDoKonsoli.qsize() > 0:
            message = kolejkaDoKonsoli.get()
            print(message)
        time.sleep(0.01)
def sendConsoleMessage(message):
    kolejkaDoKonsoli.put(message)



inputConsole = threading.Thread(target=consoleInput)
outputConsole = threading.Thread(target=consoleOutput)
inputConsole.start()
outputConsole.start()





