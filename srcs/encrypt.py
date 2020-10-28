from datetime import datetime as d
import os
import sys


BYTEORDER = sys.byteorder  # big/little
TEXTMASK = 0b10000000
IMGMASK = 0b11111110

def copy_bmp_header(from_bmp_fd, to_bmp_fd):
    from_bmp_fd.seek(10)
    offset = int.from_bytes(from_bmp_fd.read(1), BYTEORDER)
    from_bmp_fd.seek(0)
    bmp_header = from_bmp_fd.read(offset)
    to_bmp_fd.write(bmp_header)


def add_message_size(encrypted_file, container, size):
    """
    Add message size in first 32 bytes of encrypted_file
    """
    size = int.to_bytes(size, 4, BYTEORDER)
    j = 0
    while j < 4:
        byte = size[j]
        hide_byte(encrypted_file, container, byte)
        j += 1


def hide_byte(encrypted_file, container, char):
    """
    Hides one byte char in least significant bits of 8 bytes from container and writes it in encrypted_file
    """
    for i in range(0, 8):
        img_byte = int.from_bytes(container.read(1), BYTEORDER)
        img_byte &= IMGMASK

        bit = char & TEXTMASK
        bit >>= 7
        img_byte |= bit
        encrypted_file.write(img_byte.to_bytes(1, BYTEORDER))

        char <<= 1


def encrypt_text(message, img_file_name):
    """
    Hides message string in image based on img_file_name.
    img_file_name should be bmp file.
    """
    container = open(img_file_name, 'rb')
    encrypted_file_name = img_file_name[:-4] + str(int(d.now().timestamp())) + '.bmp'
    encrypted_file = open(encrypted_file_name, 'wb')

    copy_bmp_header(container, encrypted_file)
    message = message.encode('utf-8')
    add_message_size(encrypted_file, container, len(message))

    i = 0
    while i < len(message):
        byte = message[i]
        hide_byte(encrypted_file, container, byte)
        i += 1
    encrypted_file.write(container.read())

    encrypted_file.close()
    container.close()
    print(f"\nEncoding is done. You can send {encrypted_file_name} to the recipient.\n")


def encrypt_file(message_file_name, img_file_name):
    """
    Hides text from file message_file_name in image based on img_file_name.
    message_file_name should be text file.
    img_file_name should be bmp file.
    """
    message = open(message_file_name, 'rb')
    container = open(img_file_name, 'rb')
    encrypted_file_name = img_file_name[:-4] + str(int(d.now().timestamp())) + '.bmp'
    encrypted_file = open(encrypted_file_name, 'wb')

    copy_bmp_header(container, encrypted_file)

    add_message_size(encrypted_file, container, os.stat(message_file_name).st_size)

    while True:
        byte = message.read(1)
        if not byte:
            break
        byte = int.from_bytes(byte, BYTEORDER)
        hide_byte(encrypted_file, container, byte)

    encrypted_file.write(container.read())

    encrypted_file.close()
    message.close()
    container.close()
    print(f"\nEncoding is done. You can send {encrypted_file_name} to the recipient.\n")
