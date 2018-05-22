from pwn import *
import binascii

r = remote('cpushop.2018.teamrois.cn', 43000)

r.recvuntil("Command: ")
r.sendline("2")
r.recvuntil("Product ID:")
r.sendline("0")
r.recvuntil("Your order:\n")
order = r.recvline()[:-1]

(payment, sign) = order.split("&sign=")

for i in range(8, 32):
    cmd = ['/home/tosh/bin/hash_extender', '-d', payment, '-s', sign, '-a',
           '&product=Flag', '-f', 'sha256', '-l', str(i)]

    h = process(cmd)
    h.recvuntil("New signature: ")
    new_sign = h.recvline()[:-1]
    h.recvuntil("New string: ")
    new_str = binascii.unhexlify(h.recvline()[:-1])
    h.close()

    print r.recvuntil("Command: ")
    r.sendline("3")
    print r.recvuntil("Your order:")
    r.sendline("%s&sign=%s" % (new_str, new_sign))

r.interactive()
