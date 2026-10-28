import multiprocessing
import queue
import time

do_wyslania = multiprocessing.Queue()
def sendData(self):
    while True:
        start_time = time.time()
        data, bot = do_wyslania.get()
        bot.socket.sendall(data)






def send_packet(data, bot):
    do_wyslania.put(data,bot)





