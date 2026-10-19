from __future__ import annotations




def get_external_name(player):
    return player.external_name
def get_external_status(player):
    return player.connected_to_external
def set_external_compression(player, compression_value):
    player.external_compression = compression_value
def getCompression(player):
    return player.external_compression
def getName(player):
    return player.name

