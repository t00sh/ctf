from pwn import *

SEED1 = 0xa130e004
SEED2 = 0x607f7957

def xor(x, y):
    return "".join([chr(ord(x[idx]) ^ ord(y[idx])) for idx in range(len(x))])

if __name__ == '__main__':
    # SEED1
    r = remote('crypto.chal.csaw.io', 1002)
    r.recvuntil("Send me a random seed\n")
    r.send("%.16d" % SEED1)
    r.recvuntil("Encrypted flag:\n")
    c = r.recvn(128)
    k = xor(c[:16], "Encrypted Flag: ")
    flag = xor(k, c[16:32])
    r.close()

    # SEED2
    r = remote('crypto.chal.csaw.io', 1002)
    r.recvuntil("Send me a random seed\n")
    r.send("%.16d" % SEED2)
    r.recvuntil("Encrypted flag:\n")
    c = r.recvn(128)
    k = xor(c[:16], "Encrypted Flag: ")
    flag += xor(k, c[32:48])
    r.close()

    print(flag)
