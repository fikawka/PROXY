import multiprocessing
from concurrent.futures import ThreadPoolExecutor

from bot.BotsDataReceiver import BotsDataReceiver


def startThreads():
    print("test")
    with ThreadPoolExecutor(max_workers=2) as executor:
        executor.submit(BotsDataReceiver.receive_packets)
processs = multiprocessing.Process(target=startThreads)
is_enabled = False

def startBotProcess():
    global is_enabled
    if not is_enabled:
        try:
            processs.start()
            is_enabled = True

        except Exception as e:
            print("Error while starting bot process", e)
    else:
        print("Bot process already running")
        return







