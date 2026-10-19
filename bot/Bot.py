from enum import Enum

from bot.Bots import Bots





class BotState(Enum):
    HANDSHAKE = 1
    LOGIN = 2
    PLAY = 3

class Bot:
    def __init__(self, owner, socket, nick):
        self.owner = owner
        self.socket = socket
        self.nick = nick
        self.bot_states = BotState()
        self.bot_state = self.bot_states.HANDSHAKE

        Bots.all_bots.append(self)

    bot_states = BotState


