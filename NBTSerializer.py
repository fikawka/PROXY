import struct


def serialize_tag_end():
    return struct.pack('>B', 0)
def serialize_tag_compount(name ):
    tag_id = 10
    name_encoded = name.encode("utf-8")
    name_length = len(name_encoded)
    data = (struct.pack('>B', tag_id)
            + struct.pack('>H', name_length)
            + name_encoded
            )
    return data
def serialize_trash_int_array(): #test
    tag_id = 0x0B
    name = "i_spadasz"
    name_encoded = name.encode("utf-8")
    values = [2147483641]
    name_length = len(name_encoded)
    array_length = len(values)
    data = (
            struct.pack('>B', tag_id)
            + struct.pack('>H', name_length)
            + name_encoded
            + struct.pack('>i', 2147483641))
    return data

