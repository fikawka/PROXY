import multiprocessing
import queue
import socket
import time
from concurrent.futures import ThreadPoolExecutor

from server_packets.ChatMessagePacket import ChatMessagePacket


class PortScanner:
    def __init__(self,host,port_min, port_max, player):
        self.host = host
        self.port_min = port_min
        self.port_max = port_max
        self.port_queue = self.generatePorts()
        self.ports_found = []
        self.process = multiprocessing.Process(target=self.runsthreads)
        self.process.daemon = True
        self.finished = False
        self.player = player

    def runScanner(self):
        self.process.start()

    def runsthreads(self):
        with ThreadPoolExecutor(max_workers=50) as executor:
            for i in range(10):
                executor.submit(self.checkPorts, self.player, self.host )


    def checkPorts(self, player,  host):
        while self.port_queue.qsize() > 0:
            my_port = self.port_queue.get()
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(2)
            try:
                sock.connect((self.host,my_port))
                self.ports_found.append(my_port)
            except:
                pass
        if self.port_queue.qsize() == 0:
            time.sleep(2)
            if self.finished == False:
                self.finished = True
                player.sendPacket(ChatMessagePacket(message=f"Ports: {str(self.ports_found)} are open!", sender=None, color="green", ))
                return self.ports_found





    def generatePorts(self):
        start = self.port_min
        port_queue = multiprocessing.Queue()
        while start <= self.port_max:
            port_queue.put(start)
            start += 1
        return port_queue

