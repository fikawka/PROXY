from random import Random

from server_packets.KeepAlivePacket import KeepAlivePacket


class GameLogic:
    def __init__(self, player):
        self.player = player
    def update_game_logic(self):
        if self.player.tick_counter >= 25:
            self.player.tick_counter = 0
            if not self.player.connected_to_external:
                r = Random()
                additional_id = r.randint(0,255)
                self.player.do_wyslania_queue.put(KeepAlivePacket(additional_id).encode())


