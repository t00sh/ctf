import binascii
import urllib
import re

URL1 = 'http://challenges.hackover.h4q.it:8202/race'
URL2 = 'http://challenges.hackover.h4q.it:8202/ciphertext'
URL3 = 'http://challenges.hackover.h4q.it:8202/choose?driver_license=%s&color=%s'

def get_license():
    f = urllib.urlopen(URL1)
    url = f.read()
    print url
    m = re.search('"license": "(.+)"', url)

    return m.groups(1)[0]


def get_ciphertext(lic, m0, m1):
    params = urllib.urlencode({'driver_license': lic, 'm0': m0, 'm1': m1})
    f = urllib.urlopen(URL2, params)

    r = f.read()
    return r

def send_color(lic, color):
    f = urllib.urlopen(URL3 % (lic, color), "")

    url = f.read()

lic = get_license()

for i in xrange(40):
    cipher = get_ciphertext(lic, "b"*16 + "a"*16, "A"*32)
    print binascii.hexlify("".join(cipher))

    if "".join(cipher[:16]) == "".join(cipher[16:32]):
        send_color(lic, "blue")
    else:
        send_color(lic, "red")
