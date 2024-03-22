


def hex(x):
    x = bytes.fromhex(x)
    return x


def data_row(fields: list):
    answer = b'D'
    num_fields = len(fields)
    length = 6 + num_fields * 4
    for field in fields:
        length += len(str(field))
    length_as_bytes = length.to_bytes(4, "big")
    num_fields_as_bytes = num_fields.to_bytes(2, "big")
    answer += length_as_bytes + num_fields_as_bytes
    for field in fields:
        field_length = len(str(field))
        answer += field_length.to_bytes(4, "big") + field.encode("utf-8")
    return answer

def row_description(fields: list):
    answer = b'T'
    num_fields = len(fields)
    length = 6 + num_fields * 19  
    for field in fields:
        length += len(str(field))
    length_as_bytes = length.to_bytes(4, "big")
    num_fields_as_bytes = num_fields.to_bytes(2, "big")
    answer += length_as_bytes + num_fields_as_bytes
    for index, field in enumerate(fields):
        answer += str(field).encode("utf-8") + b'\x00'
        answer += b'\x00\x00@\x02'
        answer += (index + 1).to_bytes(2, "big")
        answer += b'\x00\x00\x04\x13'
        answer += b'\xff\xff'
        answer += b'\x00\x00\x00h'
        answer += b'\x00\x00'
    return answer

if __name__ == '__main__':
    x = "00000068"
    print(hex(x))

    print(row_description(["clo"]))

    # print(data_row(["John", "31"]))