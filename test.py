import os
import sys


UNDERLINED = '\033[4m'
BOLD = '\033[1m'
ITALIC = '\033[3m'
RESET = '\033[0m'


def encrypt(message_file, img_file):
	"""
	Hides text from message_file in img_file.
	img_file should be bmp.
	"""

	TEXT_MASK = 0b10000000
	IMG_MASK = 0b11111110

	encrypted_file = open('encrypted.bmp', 'wb')
	message = open(message_file, 'rb')
	container = open(img_file, 'rb')

	container.seek(10)
	offset = int.from_bytes(container.read(1), sys.byteorder)
	container.seek(0)
	bmp_header = container.read(offset)
	encrypted_file.write(bmp_header)

	while True:
		char = message.read(1)
		if not char:
			break

		char = int.from_bytes(char, sys.byteorder)
		for i in range(0, 7):
			img_byte = int.from_bytes(container.read(1), sys.byteorder)
			img_byte &= IMG_MASK

			char &= TEXT_MASK
			char >>= 7

			img_byte |= char
			encrypted_file.write(img_byte.to_bytes(1, sys.byteorder))

			char <<= 1

	encrypted_file.write(container.read())

	encrypted_file.close()
	message.close()
	container.close()


def decrypt(arg):
	print(arg)


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
