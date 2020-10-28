from .encrypt import BYTEORDER, IMGMASK


def extract_byte(encoded_bmp):
    byte = 0
    for _ in range(0, 8):
        img_byte = encoded_bmp.read(1)
        img_byte = int.from_bytes(img_byte, BYTEORDER)
        bit = img_byte & ~IMGMASK
        byte <<= 1
        byte |= bit
    return byte


def extract_message_len(encoded_bmp):
    message_len = []
    i = 0
    while i < 4:
        byte = extract_byte(encoded_bmp)
        message_len.append(byte)
        i += 1

    message_len = int.from_bytes(message_len, BYTEORDER)
    return message_len


def decrypt(encoded_bmp_file):
    decoded_message = open('decoded.txt', 'wb')
    encoded_bmp = open(encoded_bmp_file, 'rb')

    encoded_bmp.seek(10)
    offset = int.from_bytes(encoded_bmp.read(1), BYTEORDER)
    encoded_bmp.seek(offset)

    message_len = extract_message_len(encoded_bmp)

    i = 0
    while i < message_len:
        byte = extract_byte(encoded_bmp)
        decoded_message.write(byte.to_bytes(1, BYTEORDER))
        i += 1

    decoded_message.close()
    encoded_bmp.close()
    print("\nDecoding is done. You can see massage in decoded.txt\n")
