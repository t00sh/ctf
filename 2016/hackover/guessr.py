#!/usr/bin/env python3
import random
import sys
import socket

HOST = 'challenges.hackover.h4q.it'
#HOST = '127.0.0.1'
PORT = 64500

ARGS = (2**31, 7**6, 5)

def connect_to_serv(host, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((host, port))
    except:
        print "[-] Failed to connect to server"
        sys.exit(1)
    return sock


class RNG:

    def __init__(self, m, a, b, seed=None):
        self.m = m
        self.a = a
        self.b = b
        if not seed:
            seed = random.randint(0, m - 1)
        self.val = seed


    def get_val(self, lower, upper):
        rng = upper - lower
        return (self.val % rng) + lower


    def step(self, n = 1):
        for i in range(n):
            self.val = (self.a * self.val + self.b) % self.m


def get_response(sock):
    while True:
        data = sock.recv(512)

        if data is None or data == "":
            sys.exit(0)

        if data.find('too low') != -1:
            return -1
        if data.find('too high') != -1:
            return 1
        if data.find('Correct') != -1:
            return 0

def guess(sock):
    start = 0
    end = 100


    while True:
        m = (start+end)/2
        sock.send("%d\n" % m)

        resp = get_response(sock)

        if resp == 0:
            return m
        elif resp < 0:
            start = m+1
        else:
            end = m-1

def get_list(sock, n):
    L = []

    for i in xrange(n):
        L.append(guess(sock))
    return L

def get_state(seq):
    for seed in xrange(0xFFFFFFFF):
        rng = RNG(*ARGS, seed=seed)
        found = True

        if seed % 10000000 == 0:
            print "Seed = %d" % seed

        for i in xrange(len(seq)):
            if seq[i] != rng.get_val(1, 101):
                found = False
                break
            rng.step()

        if found:
            print "Seed = %d" % seed
            return rng
    return None

sock = connect_to_serv(HOST, PORT)

seq = get_list(sock, 10)

print "Seq = %s" % seq

rng = get_state(seq)



for guesses in xrange(10):
    print "Guesses = %d" % guesses
    sock.send("%d\n" % rng.get_val(1, 101))
    rng.step()

while True:
    data = sock.recv(1024)

    if data is None or data == "":
        sys.exit(0)
    if data.find('flag') != -1:
        print data[data.find('flag'):]
