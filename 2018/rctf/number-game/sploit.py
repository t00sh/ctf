from pwn import *
from hashlib import sha256
import itertools
import string


def puzzle(r):
    r.recvuntil("****+")
    known = r.recvn(16)

    r.recvuntil(' == ')
    sha = r.recvline()[:-1]

    r.recvuntil(" XXXX:")

    for p in itertools.product(string.ascii_letters + string.digits, repeat=4):
        p = "".join(list(p))
        if sha256(p + known).hexdigest() == sha:
            r.sendline(p)
            break

def is_word(w, guess, true, bad):
    c_true = 0
    c_bad = 0

    for i in range(4):
        if w[i] == guess[i]:
            c_true += 1
        elif w[i] in guess:
            c_bad += 1
    return c_true == true and c_bad == bad

def solve(r):
    possibles = [0,1,2,3,4,5,6,7,8,9]
    tries = []
    S = map(list, list(itertools.permutations(possibles, 4)))
    guess = S[0]

    for i in range(6):
        r.sendline(" ".join(map(str, guess)))
        try:
            print r.recvuntil("Nope. ", timeout=2)
            (well, bad) = map(int, r.recvline()[:-1].split(","))
            print well, bad
            tries.append((guess, well, bad))
            S = filter(lambda x: is_word(x, guess, well, bad), S)
            guess = random.choice(S)
        except:
            return False

    return True

r = remote('149.28.139.172', 10002)
puzzle(r)

for i in range(8):
    solve(r)
r.interactive()
