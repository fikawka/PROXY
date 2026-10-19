from Packet import Packet


class WindowItemsPacket(Packet):
    def __init__(self):
        super().__init__(packet_id=b'\x30')
        