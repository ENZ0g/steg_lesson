import os


UL = '\033[4m'  # underlined
BD = '\033[1m'  # bold
IC = '\033[3m'  # italic
RT = '\033[0m'  # reset style


def print_man(app_name):
    print(f"{BD}SYNOPSIS{RT}")
    print(f"\t{BD}{app_name}{RT} {BD}-e{RT} {UL}message_file{RT} {UL}container_file{RT}")
    print(f"\t{BD}{app_name}{RT} {BD}-ei{RT} {UL}container_file{RT}")
    print(f"\t{BD}{app_name}{RT} {BD}-d{RT} {UL}img_file{RT}")
    print()
    print(f"{BD}DESCRIPTION{RT}")
    print(f"\t{BD}{app_name}{RT} hides your message from {UL}message_file{RT} or STDIN in the image based on " +
          f"{UL}container_file{RT} by replacing least significant bit, or recovers message from {UL}img_file{RT}.\n" +
          f"\t{UL}message_file{RT} should be text file.\n" +
          f"\t{UL}container_file{RT} should be bmp file.\n" +
          f"\t{UL}img_file{RT} should be bmp file.\n")
    print(f"{BD}OPTIONS{RT}")
    print(f"\t{BD}-e{RT}", end='')
    print(f"\tEncryption mode. Hides the message from {UL}message_file{RT} in the image based on {UL}container_file{RT}.")
    print(f"\t{BD}-ei{RT}", end='')
    print(f"\tEncryption mode. Hides the message from {BD}STDIN{RT} in the image based on {UL}container_file{RT}.")
    print(f"\t{BD}-d{RT}", end='')
    print(f"\tDecryption mode. Recovers the message from {UL}img_file{RT}. Writes the message in {IC}decoded.txt{RT}.")
    print(f"\t{BD}-h{RT}", end='')
    print("\tShow this man.")
