from Crypto.Util.number import inverse, bytes_to_long, long_to_bytes
from pwn import *

def s2n(s):
    return bytes_to_long(bytearray(s, 'latin-1'))

def n2s(n):
    return long_to_bytes(n).decode('latin-1')

def gcd(x, y):
   while(y):
       x, y = y, x % y
   return x

def inv_mod(a, b):
    mod = b
    x0, x1, y0, y1 = 0, 1, 1, 0
    while a != 0:
        q, b, a = b // a, a, b % a
        y0, y1 = y1, y0 - q * y1
        x0, x1 = x1, x0 - q * x1
    return x0 % mod

def encrypt(r, c):
    r.recvuntil("4. encrypt")
    r.sendline("4")
    r.sendline(c)
    r.recvuntil("input the data:")
    return int(r.recvline()[:-1], 16)

def recover_n(r):
    plains, ciphers = [],[]
    for i in range(4):
        c = encrypt(r, chr(2 + i))
        plains.append(2 + i)
        ciphers.append(c)

    n = ciphers[0] - pow(plains[0], 0x10001)
    for i in range(1, 4):
        n = -gcd(n, ciphers[i] - pow(plains[i], 0x10001))
    return n


def recover_fake_flag(r):
    r.recvuntil("4. encrypt")
    r.clean(1.0)
    r.sendline("3")
    return int(r.recvline()[:-1], 16)

def recover_flag(r):
    r.recvuntil("4. encrypt")
    r.clean(1.0)
    r.sendline("1")
    return int(r.recvline()[:-1], 16)

if __name__ == '__main__':
    r = remote('crypto.chal.csaw.io', 1001)

    n = recover_n(r)
    fake_flag_ko = recover_fake_flag(r)
    flag = recover_flag(r)

    for i in range(10000):
        fake_flag = 'fake_flag{%s}' % (('%X' % i).rjust(32, '0'))

        m = s2n(fake_flag)
        g = gcd(fake_flag_ko - pow(m, 0x10001, n), n)
        if g != 1 and g != n:
            break

    p = n // g
    q = n // p
    d = inv_mod(0x10001, (p - 1) * (q - 1))
    m = pow(flag, d, n)
    print(n2s(m))
