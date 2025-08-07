from Crypto.Util.number import *
import os

# Get directory where this script is located
script_dir = os.path.dirname(os.path.abspath(__file__))
out_path = os.path.join(script_dir, "out.txt")

def xor(data, key):
    return bytes([b ^ key[i % len(key)] for i, b in enumerate(data)])

with open(out_path, "rb") as f:
    ciphertext = f.read()

known_plaintext = b"sctf{"
recovered_key = xor(ciphertext[:5], known_plaintext)
decrypted = xor(ciphertext, recovered_key)

print("Decrypted:", decrypted.decode('utf-8', errors='replace'))