#!/usr/bin/python3
from pwn import *
import base64
from PIL import Image
from io import BytesIO

conn = remote('challenges.shutlock.fr',50001)
conn.sendline(b'go')

key = conn.recv()
print(f"KEY = {key.decode()}")
conn.send(b'ack')
img_chunk = conn.recv()

j = 0
while j < 50:
    i = 0
    while len(img_chunk.decode()) > 5:
        print(f"CHUNK = {img_chunk.decode()}")
        if i == 0:
            img_begin = base64.b64decode(img_chunk.decode())
            if img_begin[0] == 137:
                conn.send(b'non-dopante')
            else:
                conn.send(b'dopante')
        img_chunk = conn.recv()
        i += 1
    conn.send(b'ack')
    img_chunk = conn.recv()
    j += 1