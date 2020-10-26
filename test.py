import os
import sys


UNDERLINED = '\033[4m'
BOLD = '\033[1m'
ITALIC = '\033[3m'
RESET = '\033[0m'
TEXTMASK = 0b10000000
IMGMASK = 0b11111110




def copy_bmp_header(from_bmp_fd, to_bmp_fd):
	from_bmp_fd.seek(10)
	offset = int.from_bytes(from_bmp_fd.read(1), sys.byteorder)
	from_bmp_fd.seek(0)
	bmp_header = from_bmp_fd.read(offset)
	to_bmp_fd.write(bmp_header)


def encrypt(message_file, img_file):
	"""
	Hides text from message_file in img_file.
	img_file should be bmp.
	"""
	encrypted_file = open('encrypted.bmp', 'wb')
	message = open(message_file, 'rb')
	container = open(img_file, 'rb')

	print('to_encrypt file size:', os.stat(message_file).st_size)

	copy_bmp_header(container, encrypted_file)
	n = 1
	while True:
		char = message.read(1)
		if not char:
			break
		char = int.from_bytes(char, sys.byteorder)
		print('-', char)
		for i in range(0, 8):
			img_byte = int.from_bytes(container.read(1), sys.byteorder)
			img_byte &= IMGMASK

			bit = char & TEXTMASK
			bit >>= 7
			img_byte |= bit
			print(img_byte)
			encrypted_file.write(img_byte.to_bytes(1, sys.byteorder))
			print(n, img_byte.to_bytes(1, sys.byteorder))
			n += 1

			char <<= 1

	encrypted_file.write(container.read())

	encrypted_file.close()
	message.close()
	container.close()


def decrypt(encoded_bmp_file, message_len):
	decoded_message = open('decoded.txt', 'wb')
	encoded_bmp = open(encoded_bmp_file, 'rb')

	encoded_bmp.seek(10)
	offset = int.from_bytes(encoded_bmp.read(1), sys.byteorder)
	encoded_bmp.seek(offset)

	i = 0
	while i < int(message_len):
		char = 0

		for j in range(0, 8):
			img_byte = encoded_bmp.read(1)
			print('raw', img_byte)
			img_byte = int.from_bytes(img_byte, sys.byteorder)
			print('int', img_byte)
			byte = img_byte & 0b00000001
			char <<= 1
			char |= byte
		print('*', char)
		decoded_message.write(char.to_bytes(1, sys.byteorder))
		i += 1

	decoded_message.close()
	encoded_bmp.close()


def print_man():
	print(f"{UNDERLINED}Encrypt mode:{RESET} python3 {BOLD}code.py{RESET} {ITALIC}file_to_encrypt bmp_file{RESET}")
	print(f"{UNDERLINED}Decrypt mode:{RESET} python3 {BOLD}code.py{RESET} {ITALIC}bmp_file message_len{RESET}")


if len(sys.argv) < 2:
	print("Error: too few arguments\n")
	print_man()
	sys.exit(1)
elif len(sys.argv) > 3:
	print("Error: too many arguments\n")
	print_man()
	sys.exit(1)


while True:
	print("Choose mode:\n1 - encrypt\n2 - decrypt\n3 - exit")
	choice = input()
	if choice == '1':
		encrypt(sys.argv[1], sys.argv[2])
	elif choice == '2':
		decrypt(sys.argv[1], sys.argv[2])
	elif choice == '3':
		break
	else:
		print('\nNo such option!\n')
