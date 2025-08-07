1. Opening up the binary in Ghidra, we can find:
```
if ((local_88 < 0x21) &&
   (piVar4 = (int *)std::vector<int,std::allocator<int>>::operator[](local_68,local_88),
   *piVar4 != *(int *)(password + local_88 * 4))) {
    bVar2 = true;
}
```
This function compares user input against a fixed password array that is 0x21 (33 characters)long, and compares integers in groups of 4 bytes (little-endian).
```
if ((cVar1 < '!') || (cVar1 == '\x7f')) {
    std::operator<<((ostream *)std::cout,"Illegal character detected\n");
}
```
This function only allows user input to be in printable ASCII, and rejects 0x7f (DEL character).
```
std::vector<int,std::allocator<int>>::push_back(local_68,(int *)(mapping + (long)(cVar1 + -0x21) * 4));
```
This function maps input characters to 4-byte integers in little-endian.

2. In order to find more information about the mapping, I viewed the binary in Hex Rays using Dogbolt:
```
std::vector<int>::push_back((unsigned __int64)v15, &mapping[v8 - 33]);
```
This shows that the input characters are converted to integers by subtracting 33.

3. Using this information, I created a script solve.py to reconstruct the password by finding which character maps to which password value. My final output was `Recovered password: sctf{50m30n3_g1v3_7h15_guy_4_m4p}`. 