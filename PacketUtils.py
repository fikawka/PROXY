class PacketUtils:
    @staticmethod
    def read_varint_from_buffer(bufer):
        """Pomocnicza funkcja czytająca VarInt z początku self.buffer"""
        num_read = 0
        result = 0
        while True:
            if num_read >= len(bufer):
                raise ValueError("Za mało danych na VarInt")

            read_byte = bufer[num_read]
            value = read_byte & 0x7F
            result |= value << (7 * num_read)
            num_read += 1

            if (read_byte & 0x80) == 0:
                break

            if num_read > 5:
                raise ValueError("VarInt jest za długi!")

        return result, num_read
    @staticmethod
    def read_varint_from_bytes(data_bytes, offset=0):
        """Czyta VarInt z dowolnego obiektubytes/bytearray od wskazanego offsetu"""
        num_read = 0
        result = 0

        while True:
            if offset + num_read >= len(data_bytes):
                raise ValueError("Za mało danych na VarInt")

            read_byte = data_bytes[offset + num_read]
            value = read_byte & 0x7F
            result |= value << (7 * num_read)
            num_read += 1

            if (read_byte & 0x80) == 0:
                break

            if num_read > 5:
                raise ValueError("VarInt jest za długi!")

        return result, num_read