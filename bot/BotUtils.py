from random import Random

from bot.Bots import Bots


def generateId():
    r = Random()
    id = r.randint(1,9999)
    for bot in Bots.all_bots:
        if bot.id == id:
            generateId()
            return
    return id

