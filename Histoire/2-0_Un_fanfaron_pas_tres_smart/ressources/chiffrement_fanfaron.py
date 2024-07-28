#!/usr/bin/env python3
from Crypto.Util.number import bytes_to_long, getPrime
from secret import text

def generate_key():
    p = getPrime(2048)
    N = pow(p,3)
    e = 0x10001
    return (N,e)

N,e = generate_key()
pt = bytes_to_long(text.encode())
ct = pow(pt, e, N)

print(f"N = {N}")
print(f"e = {e}")
print(f"ct = {ct}")
