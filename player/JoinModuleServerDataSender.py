import threading
import time
from queue import Queue

from independent_modules import Console


class JoinModuleServerDataSender:
    def __init__(self):
        self.to_server_send_queue = Queue()
        self.ready_event =threading.Event()
    def send_packet_loop(self, player, socket):
        while player.player_state == player.player_states.CONNECTED_TO_EXTERNAL_SERVER:
            timee = time.time()
            while not self.to_server_send_queue.empty():
                pakiet = self.to_server_send_queue.get()
                try:
                    socket.sendall(pakiet)
                except Exception as e:
                    Console.sendConsoleMessage(e)
                    player.joiner.quit()

                    break
            time_elapsed = time.time() - timee
            if time_elapsed < 0.01:
                time.sleep(0.01 - time_elapsed)



