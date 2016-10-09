import sys
import socket
import base64
import subprocess
from Crypto.Cipher import AES


def connect_to_serv(host, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((host, port))
    except:
        print "[-] Failed to connect to server"
        sys.exit(1)
    return sock


def get_dice_roll(sock):

    while True:
        data = sock.recv(1024)
        if data == None or data == "":
            return None
        if data.find("My dice roll: ") != -1:
            return base64.b64decode(data[data.find('My dice roll: ')+14:])

def get_key(sock):
    while True:
        data = sock.recv(1024)
        if data == None or data == "":
            return None

        if data.find("My key: ") != -1:
            return base64.b64decode(data[data.find('My key: ')+8:])

def encrypt(m,k):
    cipher = AES.new(k, AES.MODE_ECB)
    return cipher.encrypt(m)

def decrypt(m,k):
    cipher = AES.new(k, AES.MODE_ECB)
    return cipher.decrypt(m)

def get_rand(n):
    p = subprocess.Popen('./test %d' % n, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    return int(p.stdout.readline())

def get_seq(n):
    L = []

    for i in xrange(n):
        sock = connect_to_serv('challenges.hackover.h4q.it', 1415)

        dice = get_dice_roll(sock)
        sock.send("test\n")
        key = get_key(sock)
        sock.send("test\n")
        dice = ord(decrypt(dice, key)[1])

        L.append(dice)
    return L

def check_seq(seq, start):
    n = 0
    k = start

    while n < len(seq):
        x = get_rand(k)
        if seq[n] == x:
            n += 1
        else:
            n = 0
        k += 1
        print k, n
    return k

seq = get_seq(12)
print seq
seed = check_seq(seq, 5900)


for j in xrange(0xfffff):
    sock = connect_to_serv('challenges.hackover.h4q.it', 1415)

    found = False

    for i in xrange(32):
        print "Iteration %d" % i
        k = "\x01"*16
        n = get_rand(i+seed+15+j*2)
        dice = get_dice_roll(sock)
        if dice == None:
            break
        sock.send(base64.b64encode(encrypt("\x00" + chr(7-n) + "\x01"*14, k)) + "\n")
        key = get_key(sock)
        if key == None:
            break
        sock.send(base64.b64encode(k) + "\n")
        dice = ord(decrypt(dice, key)[1])

        if i == 31:
            found = True
    if found:

        while True:
            data = sock.recv(1024)
            if data == None or data == "":
                sys.exit(0)
            print data
