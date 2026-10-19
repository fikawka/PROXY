import time
from random import Random

from player import PacketChecker
from player.GameLogic import GameLogic


class PlayerDataSenderLoop:
    def __init__(self, player):
        self.player = player
        self.target_tps = 20
        self.tick_interval = 1.0 / self.target_tps

    def tick_loop(self):           # Jezeli jest polaczony z lobby ale nie z externalem

        while self.player.isconnected:
            start_time = time.time()
            # 1. OPRÓŻNIAMY KOLEJKĘ: Wyciągamy WSZYSTKIE pakiety,
            # które wątek sieciowy wrzucił przez ostatnie 50 milisekund
            while not self.player.packet_queue.empty():
                packet_data = self.player.packet_queue.get()
                if self.player.player_state == self.player.player_states.CONNECTED_TO_PROXY_LOBBY:
                    self.player.player_packet_handler.handle_packet(packet_data)
                elif self.player.player_state == self.player.player_states.CONNECTED_TO_EXTERNAL_SERVER:
                    PacketChecker.check_and_pass_outgoing(player=self.player, packet_data=packet_data)

                    #print("LOL") dziala
            self.player.tick_counter += 1
            self.player.gamelogic.update_game_logic()
            while not self.player.do_wyslania_queue.empty():
                pakiet_data = self.player.do_wyslania_queue.get()
                try:
                    self.player.client_socket.sendall(pakiet_data)
                except Exception as e:
                    print(f"error: {e}")
                    self.player.disconnect()
                    break

            elapsed = time.time() - start_time
            sleep_time = self.tick_interval - elapsed
            if sleep_time > 0:
                time.sleep(sleep_time)


