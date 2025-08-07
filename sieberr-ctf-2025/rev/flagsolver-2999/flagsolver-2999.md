1. When using Ghidra to analyse the binary, we can see:
```
  local_38[0] = 0x14;
  local_38[1] = 4;
  local_38[2] = 0x13;
  local_38[3] = 1;
  local_38[4] = 0x1c;
  local_38[5] = 0x22;
  local_38[6] = 0xb;
  local_38[7] = 0x54;
  local_38[8] = 10;
  local_38[9] = 0x54;
  local_38[10] = 9;
  local_38[0xb] = 0x50;
  local_38[0xc] = 0x53;
  local_38[0xd] = 0x15;
  local_38[0xe] = 0x1e;
  local_38[0xf] = 0x38;
  local_38[0x10] = 1;
  local_38[0x11] = 0xb;
  local_38[0x12] = 0x53;
  local_38[0x13] = 0x51;
  local_38[0x14] = 0x38;
  local_38[0x15] = 4;
  local_38[0x16] = 0xf;
  local_38[0x17] = 0x54;
  local_38[0x18] = 4;
  local_38[0x19] = 0xc;
  local_38[0x1a] = 2;
  local_38[0x1b] = 0x15;
  local_38[0x1c] = 0x38;
  local_38[0x1d] = 0x5f;
  local_38[0x1e] = 0x57;
  local_38[0x1f] = 0x54;
  local_38[0x20] = 0x56;
  local_38[0x21] = 0x55;
  local_38[0x22] = 0x51;
  local_38[0x23] = 0x52;
  local_38[0x24] = 3;
  local_38[0x25] = 0x1a;
```
This is likely a list of bytes that make up the flag. Additionally, we can see:
```
  for (local_6c = 0; local_6c < 0x26; local_6c = local_6c + 1) {
    if ((uint)(local_38[(int)local_6c] ^ 0x67) != (int)local_68[(int)local_6c]) {
      bVar1 = false;
    }
  }
```
This is a validation loop that works by taking each byte in local_38 listed above, and XORing it with 0x67. This means that the flag can be recovered by: `flag_byte = encrypted_byte ^ 0x67`.

2. Since there is a large amount of bytes in local_38, I decided to use z3-solver to automate the process. I wrote a z3-solver script in solve.py that performs the XOR operation `flag_byte = encrypted_byte ^ 0x67` for each byte in local_38 and outputs the flag. My final output was: `Found valid flag: sctf{El3m3n74ry_fl46_ch3cker_8031265d}`.