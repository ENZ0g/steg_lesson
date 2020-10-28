from srcs.decrypt import decrypt
from srcs.encrypt import encrypt_file, encrypt_text
from srcs.man import print_man
import os
import sys


if len(sys.argv) == 1:
    print('To few arguments!\nUse -h to see man')
elif sys.argv[1] == '-e' and len(sys.argv) == 4:
    encrypt_file(sys.argv[2], sys.argv[3])
elif sys.argv[1] == '-ei':
    encrypt_text(input("Enter you message:\n"), sys.argv[2])
elif sys.argv[1] == '-d':
    decrypt(sys.argv[2])
elif sys.argv[1] == '-h':
    print_man(__file__.split(os.sep)[-1])
else:
    print("Incorrect arguments!\nUse -h to see man")
