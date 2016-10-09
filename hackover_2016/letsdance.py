#!/usr/bin/env python3
import random
import sys
import socket
import base64
import binascii

HOST = 'challenges.hackover.h4q.it'
#HOST = '127.0.0.1'
PORT = 16335


def connect_to_serv(host, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((host, port))
    except:
        print "[-] Failed to connect to server"
        sys.exit(1)
    return sock

def encrypt(sock, msg):
    sock.send("encrypt\n")
    sock.send(base64.b64encode(msg) + "\n")

    while True:
        data = sock.recv(2048)

        if data is None or data == "":
            sys.exit(0)

        for l in data.split("\n"):
            if len(l) > 80:
                return l

def get_flag(sock):
    sock.send("gimmeflag\n")

    while True:
        data = sock.recv(2048)

        if data is None or data == "":
            sys.exit(0)
        for l in data.split("\n"):
            if len(l) > 80:
                return l

def decrypt_flag(cipher, flag, plain):
    f = ""
    for i in xrange(len(cipher)):
        f += chr(ord(cipher[i]) ^ ord(flag[i]) ^ ord(plain[i]))

    return f

print "[+] Connect to %s:%d" % (HOST, PORT)
sock = connect_to_serv(HOST, PORT)


charset =  [chr(ord('a')+i) for i in xrange(26)]
charset += [chr(ord('A')+i) for i in xrange(26)]
charset += [chr(ord('0')+i) for i in xrange(10)]

print "[+] Finding a nonce collision..."

for i in charset:
    for j in charset:
        flag = base64.b64decode(get_flag(sock))

        flag_nonce = flag[:24]
        flag = flag[40:]

        plain = "A"*32 + i+j

        c = encrypt(sock, plain)
        c = base64.b64decode(c)

        nonce = c[:24]
        cipher = c[40:]

        if flag_nonce == nonce:
            print "[+] Collision found !"
            print " * Nonce          : %s" % binascii.hexlify(nonce)
            print " * Plain          : %s" % binascii.hexlify(plain)
            print " * Cipher         : %s" % binascii.hexlify(cipher)
            print " * Flag encrypted : %s" % binascii.hexlify(flag)

            flag = decrypt_flag(cipher, flag, plain)

            print " * Flag           : %s" % flag

            sys.exit(0)
