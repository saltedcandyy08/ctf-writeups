1. From the challenge title, we can tell that this is about XOR. Looking at the gen.py script, we find:
```def xor(data: bytes, key: bytes) -> bytes:
    return bytes([b ^ key[i % len(key)] for i, b in enumerate(data)])
```
This function applies XOR to each byte in `data` with the corresponding byte in `key`. If `key` is shorter than `data`, it repeats cyclically.
The XOR function can be written as: ciphertext = plaintext ^ key 
```key = os.urandom(5)``` shows that it generates a 5-byte key randomly.
The ciphertext is then saved in out.txt, and we have to reverse this XOR to obtain the original flag.txt.

2. Since we know that the flag format is "sctf{...}", we can XOR the first 5 bytes of the ciphertext in out.txt with the flag plaintext. 
Since we know that ```ciphertext = plaintext ^ key```, 
Therefore we obtain this XOR relationship: ```key = ciphertext ^ plaintext```.
Hence, we can try to recover the key by XORing the first 5 bytes of the ciphertext with the flag plaintext as shown below:
```
    known_plaintext = b"sctf{"
    recovered_key = xor(ciphertext[:5], known_plaintext)
```

3. Then, using the key, we can XOR the plaintext with the key to get the original ciphertext that was in flag.txt:
```decrypted = xor(ciphertext, recovered_key)```
In order to represent the ciphertext bytes in a readable form, we decode it using utf-8:
```print("Decrypted:", decrypted.decode('utf-8', errors='replace'))```
I ran the soln.py script and obtained the flag successfully: ```Decrypted: sctf{x0rc3ry_1nd3ed}```
