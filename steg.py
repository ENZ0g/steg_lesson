import os
import sys
from datetime import datetime as d


UNDERLINED = '\033[4m'
BOLD = '\033[1m'
ITALIC = '\033[3m'
RESET = '\033[0m'
TEXTMASK = 0b10000000
IMGMASK = 0b11111110
FILENAME = __file__.split(os.sep)[-1]


def copy_bmp_header(from_bmp_fd, to_bmp_fd):
	from_bmp_fd.seek(10)
	offset = int.from_bytes(from_bmp_fd.read(1), sys.byteorder)
	from_bmp_fd.seek(0)
	bmp_header = from_bmp_fd.read(offset)
	to_bmp_fd.write(bmp_header)


def add_message_size(encrypted_file, container, size):
	size = int.to_bytes(size, 4, sys.byteorder)
	print('size', size)
	j = 0
	while j < 4:
		byte = size[j]
		print('byte', byte)
		for i in range(0, 8):
			img_byte = int.from_bytes(container.read(1), sys.byteorder)
			img_byte &= IMGMASK

			bit = byte & TEXTMASK
			bit >>= 7
			img_byte |= bit
			encrypted_file.write(img_byte.to_bytes(1, sys.byteorder))
			byte <<= 1
		j += 1


def encrypt(message_file, img_file):
	"""
	Hides text from message_file in img_file.
	img_file should be bmp.
	"""
	message = open(message_file, 'rb')
	container = open(img_file, 'rb')
	encrypted_file_name = img_file[:-4] + str(int(d.now().timestamp())) + '.bmp'
	encrypted_file = open(encrypted_file_name, 'wb')

	print('to_encrypt file size:', os.stat(message_file).st_size)

	copy_bmp_header(container, encrypted_file)

	add_message_size(encrypted_file, container, os.stat(message_file).st_size)

	while True:
		char = message.read(1)
		if not char:
			break
		char = int.from_bytes(char, sys.byteorder)
		for i in range(0, 8):
			img_byte = int.from_bytes(container.read(1), sys.byteorder)
			img_byte &= IMGMASK

			bit = char & TEXTMASK
			bit >>= 7
			img_byte |= bit
			encrypted_file.write(img_byte.to_bytes(1, sys.byteorder))

			char <<= 1

	encrypted_file.write(container.read())

	encrypted_file.close()
	message.close()
	container.close()
	print(f"\nEncoding is done. You can send {encrypted_file_name} to the recipient.\n")


def extract_message_len(encoded_bmp):
	message_len = []

	j = 0
	while j < 4:
		byte = 0
		for i in range(0, 8):
			img_byte = encoded_bmp.read(1)
			img_byte = int.from_bytes(img_byte, sys.byteorder)
			bit = img_byte & ~IMGMASK
			byte <<= 1
			byte |= bit
		message_len.append(byte)
		j += 1

	message_len = int.from_bytes(message_len, sys.byteorder)
	print(message_len)
	return message_len


def decrypt(encoded_bmp_file):
	decoded_message = open('decoded.txt', 'wb')
	encoded_bmp = open(encoded_bmp_file, 'rb')

	encoded_bmp.seek(10)
	offset = int.from_bytes(encoded_bmp.read(1), sys.byteorder)
	encoded_bmp.seek(offset)

	message_len = extract_message_len(encoded_bmp)

	i = 0
	while i < int(message_len):
		char = 0

		for j in range(0, 8):
			img_byte = encoded_bmp.read(1)
			img_byte = int.from_bytes(img_byte, sys.byteorder)
			byte = img_byte & ~IMGMASK
			char <<= 1
			char |= byte
		decoded_message.write(char.to_bytes(1, sys.byteorder))
		i += 1

	decoded_message.close()
	encoded_bmp.close()
	print("\nDecoding is done. You can see massage in decoded.txt\n")


def print_man():
	print(f"{UNDERLINED}Encrypt mode:{RESET} python3 {BOLD}{FILENAME}{RESET} {ITALIC}file_to_encrypt bmp_file{RESET}")
	print(f"{UNDERLINED}Decrypt mode:{RESET} python3 {BOLD}{FILENAME}{RESET}")


# if len(sys.argv) < 2:
# 	print("Error: too few arguments\n")
# 	print_man()
# 	sys.exit(1)
if len(sys.argv) > 3:
	print(f"{FILENAME}: Error: too many arguments\n")
	print_man()
	sys.exit(1)


while True:
	print("Choose mode:\n1 - encrypt\n2 - decrypt\n3 - help\n4 - exit")
	choice = input()
	if choice == '1':
		try:
			encrypt(sys.argv[1], sys.argv[2])
		except IndexError:
			file_to_encrypt = input("Enter the name of the text file to encrypt (you can skip this step and enter message later):\n")
			bmp_file = input("Enter the name of the image file (it should be bmp):\n")
			if os.path.isfile(file_to_encrypt) and os.path.isfile(bmp_file):
	elif choice == '2':
		decrypt(sys.argv[1])
	elif choice == '3':
		print_man()
	elif choice == '4':
		break
	else:
		print('\nNo such option!\n')
