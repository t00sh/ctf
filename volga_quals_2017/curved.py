from curved_server import *
import socket
import re

if __name__ == '__main__':
    cmd1 = 'exit'
    cmd2 = 'leave'


    # Import known signatures
    (r, s1) = import_cmd_signature(cmd1, '.')
    (r, s2) = import_cmd_signature(cmd2, '.')

    # Hash the two commands
    hash1 = int(hashlib.sha512(cmd1).hexdigest(), 16) >> (512 - bit_length(n))
    hash2 = int(hashlib.sha512(cmd2).hexdigest(), 16) >> (512 - bit_length(n))

    # Calculate the private 'k'
    k  = ((hash1 - hash2) * invert(s1 - s2, n)) % n

    # Calculate the private key
    sk = (((s1 * k) - hash1) * invert(r, n)) % n

    # Create signature object
    sig = ECDSA(G, int(sk))

    # We can now create new signatures
    cmd = 'cat flag'
    (r, s) = sig.sign(cmd)

    # Connect to server
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(('curved.quals.2017.volgactf.ru', 8786))

    # Solve puzzle
    line = sock.recv(1024)
    chall = re.search("=='(.+)'", line).group(1)
    out = subprocess.check_output(['../solve_sha1', chall])
    sock.send(out + "\n")

    # Receive first line
    line = sock.recv(1024)
    print(line)

    # send our signature
    sock.send("%d %d %s\n" % (r, s, cmd))

    # Get the flag
    line = sock.recv(1024)
    print(line)
