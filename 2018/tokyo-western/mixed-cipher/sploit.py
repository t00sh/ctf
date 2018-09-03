from pwn import *
from binascii import hexlify, unhexlify
from Crypto.Cipher import AES
from MTRecover import *

e = 65537

def gcd(a, b):
    """Calculate the Greatest Common Divisor of a and b."""
    while b:
        a, b = b, a%b
    return a

def int2hex(n):
    s = "%x" % n
    if len(s) % 2 == 1:
        s = "0" + s
    return s

def decrypt(r, n):
    r.sendline("2")
    r.recvuntil("input hexencoded cipher text:")
    r.sendline(int2hex(n))
    r.recvuntil("RSA: ")
    return int(r.recvline()[:-1][-2:], 16)

def encrypt(r, n):
    r.recvuntil("get encrypted key\n")
    c = unhexlify(int2hex(n))
    r.sendline("1")
    r.recvuntil("input plain text:")
    r.sendline(c)
    r.recvuntil("RSA: ")
    rsa = int(r.recvline()[:-1], 16)
    r.recvuntil("AES: ")
    aes = unhexlify(r.recvline()[:-1])
    return (rsa, aes)

def get_key(r):
    r.recvuntil("get encrypted key\n")
    r.sendline("4")
    r.recvline()
    return int(r.recvline()[:-1], 16)

def get_flag(r):
    r.recvuntil("get encrypted key\n")
    r.sendline("3")
    r.recvline()
    r.recvline()
    return unhexlify(r.recvline()[:-1][32:])

r = remote('crypto.chal.ctf.westerns.tokyo', 5643)
key_enc = get_key(r)


#####################
# Find modulus      #
#####################
(c1,_) = encrypt(r, 0x41)
(c2,_) = encrypt(r, 0x21)

N = gcd(0x41**e - c1, 0x21**e - c2)

for i in range(2, e+1):
    if N%i == 0:
        N =  N//i

####################
# Find AES key     #
####################
i_start = 1024-137
start = 0
end = N//(2**i_start)

for i in range(i_start+1, 1024):
    parity = decrypt(r, (key_enc * pow(2**i, e, N)) % N) & 1
    if parity == 0:
        end = (start + end)//2
    else:
        start = (start + end)//2


    print i, "%x, %x" % (start, end)
    if end - start < 20:
        break

key = decrypt(r, key_enc)
key = ((start >> 8) << 8) | key
key = unhexlify(int2hex(key))

##################################
# Recover random generator state #
##################################
output = []
end = 625//4
for i in range(end+1):
    print "Get IV number %d/%d..." % (i, end)
    (_, aes) = encrypt(r, 0x21)
    output.append(int(hexlify(aes[12:16]), 16))
    output.append(int(hexlify(aes[8:12]), 16))
    output.append(int(hexlify(aes[4:8]), 16))
    output.append(int(hexlify(aes[:4]), 16))

mtr = MT19937Recover()
r2 = mtr.go(output)
iv = unhexlify(int2hex(r2.getrandbits(16*8)))

################
# Decrypt flag #
################
flag_enc = get_flag(r)
aes = AES.new(key, AES.MODE_CBC, iv)
print aes.decrypt(flag_enc)
