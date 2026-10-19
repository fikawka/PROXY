import hashlib
import uuid
from _md5 import md5


def generate_uuid(ign: str): # ta funkcja sluzy do generacji UUID wstrzykiwanego do pakietu Handshake jak jest uzywany bungee exploit
    prefixed_ign = "OfflinePlayer:" + ign
    hash_bytes = md5(prefixed_ign.encode('utf-8')).digest()
    arr = bytearray(hash_bytes)
    arr[6] = (arr[6] & 0x0f) | 0x30  # Ustawienie wersji 3
    arr[8] = (arr[8] & 0x3f) | 0x80
    final = str(arr.hex())
    finall = final[:8] + "-" + final[8:12] + "-" + final[12:16] + "-" + final[16:20] + "-" + final[20:32]
    print(finall)
    return finall
generate_uuid("E")
