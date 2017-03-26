#!/usr/bin/python

from base64 import b64decode, b64encode
import socket
import re
import subprocess
import time
import struct

HOST = 'oracle.quals.2017.volgactf.ru'
PORT = 8789
BLOCK_SIZE = 16

CIPHER = b'\xab\xb9\xe8\x22\x05\xad\xef\xa2\xfa\xdf\x37\xe5\x90\xfe\x2f\x2b\x5b\x9f\xef\x4d\xb9\x11\x88\xfb\x58\x18\xf5\xa6\x63\xa7\x10\xf3'

timestamp = 1000000

def payload(cipher, tag):
    global timestamp
    timestamp += 2
    return b64encode(b'\x00' + struct.pack('>q', timestamp) + cipher + tag)

def check_padding(sock, cipher):
    sock.send(payload(cipher, "\x00"*10) + "\n")
    time.sleep(0.025)
    l = b64decode(sock.recv(1024))

    if l[0] == "\xa3":
#        print "Mac error"
        return True

    return False

def assemble_blocks(b1, b2):
    m = "".join(map(chr, b1))
    m += "".join(map(chr, b2))

    return m

def attack_block(sock, block, blocks):
    cur = [0 for i in xrange(BLOCK_SIZE)]
    plain = [0 for i in xrange(BLOCK_SIZE)]

    for i in xrange(BLOCK_SIZE-1, -1, -1):
        found = False

        for j in xrange(i+1, BLOCK_SIZE):
                cur[j] = (BLOCK_SIZE - i) ^ plain[j] ^ blocks[block-1][j]

        for b in xrange(0, 0x100):
            cur[i] = b

            m = assemble_blocks(cur, blocks[block])

            if check_padding(sock, m):
                plain[i] = (BLOCK_SIZE - i) ^ cur[i] ^ blocks[block-1][i]
                print "[+] Plain =", plain
                found = True
                break

        if not found:
            print "Byte", i, "not found !"
            sys.exit(1)

    return plain

def split_blocks(matrix_id):
    blocks = [[] for i in xrange(len(matrix_id)/BLOCK_SIZE)]

    for i in xrange(len(matrix_id)):
        blocks[i/BLOCK_SIZE].append(ord(matrix_id[i]))

    return blocks

def block_to_text(block):
    while block[-1] <= 16:
        del block[-1]

    return "".join(map(chr, block))

def attack(sock, cipher):
    blocks = split_blocks(cipher)
    plain = ""

    for i in xrange(len(blocks)-2, 0, -1):
        print "[+] Attacking block %d" % (i)

        b = attack_block(sock, i, blocks)
        plain = block_to_text(b) + plain
        print "PLAIN = ", plain


if __name__=="__main__":
    sock = socket.socket()
    sock.connect((HOST, PORT))

    # solve puzzle
    line = sock.recv(1024)
    chall = re.search("=='(.+)'", line).group(1)
    out = subprocess.check_output(['./solve_sha1', chall])
    sock.send(out + "\n")

    attack(sock, "\x00"*16 + CIPHER)
