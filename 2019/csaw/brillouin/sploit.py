from base64 import b64encode, b64decode
from bls.scheme import *
from bplib.bp import G1Elem, G2Elem
from petlib.bn import Bn
from pwn import *
from hashlib import sha256

def hash_m(elements):
  Cstring = b",".join([str(x) for x in elements])
  return  sha256(Cstring).digest()

def get_pk(r, params, name):
    r.recvuntil(name)
    r.recvline()
    return G2Elem.from_bytes(b64decode(r.recvline()[:-1]), params[0])

def get_sig(r, params, n, text):
    r.recvuntil("what do you want to do?")
    r.sendline(n)
    r.recvuntil("you want me to sign what?")
    r.sendline(text)
    r.recvline()
    r.recvline()
    l = r.recvline()[:-1]
    return G1Elem.from_bytes(b64decode(l), params[0])

def get_flag(r, params, l, pk):
    print(l)
    print(pk)
    r.recvuntil("what do you want to do?")
    r.sendline("4")
    r.recvline()
    r.recvline()
    for s,p in l:
        print(r.recvline())
        r.sendline(b64encode(s.export()))
        print(r.recvline())
        r.sendline(b64encode(p.export()))

    print(r.recvline())
    r.sendline(b64encode(pk.export()))


if __name__ == '__main__':
    r = remote('crypto.chal.csaw.io', 1004)
    params = setup()

    pka = get_pk(r, params, "Abraham")
    pkb = get_pk(r, params, "Bernice")
    pkc = get_pk(r, params, "Chester")

    v = [params[1].random() for _ in range(0,2)]
    sk = [poly_eval(v,i) % params[1] for i in range(1, 3+1)]

    sa = params[0].hashG1(hash_m("this stuff")) * sk[0]
    sb = params[0].hashG1(hash_m("this stuff")) * sk[1]

    l = [lagrange_basis(3, params[1], i, 0) for i in range(1,3+1)]
    pkc  = l[0]*(sk[0]*params[3] - pka)
    pkc += l[1]*(sk[1]*params[3] - pkb)
    pkc += l[2]*(sk[2]*params[3])

    get_flag(r, params, [(sa, pka), (sb, pkb)], pkc)
    r.interactive()
