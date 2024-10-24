import sys

raw = bytes()
with open(sys.argv[1], "rb") as f:
    raw = f.read()

with open(sys.argv[1], "wb") as f:
    f.write(raw.replace(b'\r', b''))
