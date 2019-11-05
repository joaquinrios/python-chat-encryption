# Encoding: UTF-8
"""

"""

import socket
import select
import sys
import math


def binaryToDecimal(binary):
    # No big deal
    decimal, i, n = 0, 0, 0
    while (binary != 0):
        dec = binary % 10
        decimal = decimal + dec * pow(2, i)
        binary = binary // 10
        i += 1
    return decimal


def stringToBinary(message):
    # No big deal
    l = list(message)
    bits = ""
    for x in l:
        bits += format(ord(x), '08b') # format so it always has 8 bits. Ex. 1100 -> 00001100
    return bits


def binaryToString(message):
    # Turns big String of 1s and 0s to a list in groups of 8
    message = [binaryToDecimal(int(message[i:i + 8])) for i, m in enumerate(message) if i % 8 == 0]
    return message


def formatKeyToMessage(key, messageLength):
    # Adapts key so it's always the same length as the message
    times = int(math.ceil(messageLength / len(key)))
    fKey = ""
    for i in range(times):
        fKey += key
    if messageLength % len(key) != 0:
        fKey +=  key[:messageLength % len(key):]
    return fKey


def encrypt(message, key):
    """
        :param message (string): Message wished to be sent in plain text
        :param key (string): Key in plain text
        :return (string): Encrypted message
        """
    binMessage = stringToBinary(message)
    fKey = stringToBinary(key)
    fKey = formatKeyToMessage(fKey, len(binMessage))
    encrypted = ""
    for i in range(len(binMessage)):
        if binMessage[i] == "1" and fKey[i] == "1":
            encrypted += "0"
        elif binMessage[i] == "1" and fKey[i] == "0":
            encrypted += "1"
        elif binMessage[i] == "0" and fKey[i] == "0":
            encrypted += "0"
        elif binMessage[i] == "0" and fKey[i] == "1":
            encrypted += "1"
    return encrypted


def decrypt(binMessage, key):
    """
    :param binMessage (string): Value that was returned with encrypt function
    :param key (string): Key in plain text
    :return (string): Decrypted message
    """
    fKey = stringToBinary(key)
    fKey = formatKeyToMessage(fKey, len(binMessage))
    decrypted = ""
    message = ""
    for i in range(len(binMessage)):
        if   binMessage[i] == "1" and fKey[i] == "1":
            decrypted += "0"
        elif binMessage[i] == "1" and fKey[i] == "0":
            decrypted += "1"
        elif binMessage[i] == "0" and fKey[i] == "0":
            decrypted +="0"
        elif binMessage[i] == "0" and fKey[i] == "1":
            decrypted +="1"
    decrypted = binaryToString(decrypted)
    for c in decrypted:
        message += chr(c)
    return message


# ---

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
if len(sys.argv) != 3:
    print "Correct usage: script, IP address, port number"
    exit()
IP_address = str(sys.argv[1])
Port = int(sys.argv[2])
server.connect((IP_address, Port))

while True:
    sockets_list = [sys.stdin, server]
    read_sockets,write_socket, error_socket = select.select(sockets_list, [], [])
    for socks in read_sockets:

        # receive message
        if socks == server:
            message = socks.recv(2048)
            print message

        # send message
        else:
            message = sys.stdin.readline().rstrip("\n")

            # encrypt the message
            secretMessage = encrypt(message, "secret")

            server.send(secretMessage)
            sys.stdout.write("<You>")
            sys.stdout.write(secretMessage)
            sys.stdout.flush()

server.close()