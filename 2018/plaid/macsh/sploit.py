from pwn import *

def msg(mac, cmdline):
    return "%s<|>%s" % (mac, cmdline)

def getmac(r, cmdline, mac='abc'):
    r.recvuntil("|$|>")
    r.sendline(msg(mac, cmdline))
    r.recvuntil(" ")
    res = r.recvline()[:-1]
    r.recvuntil("|$|>")
    return res

if __name__ == '__main__':
    # r = process("/usr/bin/python macsh.py".split(" "), stderr=2)
    r = remote('macsh.chal.pwning.xxx', 64791)

    #cmd = 'ls .////////////'
    cmd = 'cat .///flag.txt'

    mac = getmac(r, "tag " + ("echo " + "A"*11) * 256 + cmd)
    cmdline = cmd + (b" "*(256*16))

    r.sendline(msg(mac, cmdline))
    r.interactive()
