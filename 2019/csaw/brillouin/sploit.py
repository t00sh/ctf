from base64 import b64encode, b64decode
from bls.scheme import *
from bplib.bp import G1Elem, G2Elem
from petlib.bn import Bn
from pwn import *
from hashlib import sha256

def inv_mod(a, b):
    mod = b
    x0, x1, y0, y1 = 0, 1, 1, 0
    while a != 0:
        q, b, a = b // a, a, b % a
        y0, y1 = y1, y0 - q * y1
        x0, x1 = x1, x0 - q * x1
    return x0 % mod

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
    r.recvuntil("what do you want to do?")
    r.sendline("4")
    r.recvline()
    r.recvline()
    for s,p in l:
        r.sendline(b64encode(s.export()))
        r.sendline(b64encode(p.export()))

    r.clean(1.0)
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

    # We have:
    #   pka = sk1*g2
    #   pkb = sk2*g2
    #   pkc = sk3*g2
    # We want:
    #   l1*sk1'*g1 + l2*sk2'*g1 = L1*sk1'*g2 + L2*sk2'*g2 + L3*sk3'*g2
    # We set:
    #   sa = l1*sk1'*g1
    #   sb = l2*sk2'*g1
    #   pka = pka
    #   pkb = pkb
    #   pkc = sk3' + L3^(-1)*(L1*sk1'*g2 - pka + L2*sk2'*g2 - pkb)

    l = [lagrange_basis(3, params[1], i, 0) for i in range(1,3+1)]
    l2_inv = inv_mod(l[2], params[1])

    pkc  = l2_inv*l[0]*(sk[0]*params[3] - pka)
    pkc += l2_inv*l[1]*(sk[1]*params[3] - pkb)
    pkc += (sk[2]*params[3])

    get_flag(r, params, [(sa, pka), (sb, pkb)], pkc)
    r.interactive()
