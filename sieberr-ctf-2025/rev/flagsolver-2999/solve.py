from z3 import *

def solve_flag():
    # Create solver instance
    s = Solver()
    
    # The encrypted byte array from the binary
    encrypted = [
        0x14, 0x04, 0x13, 0x01, 0x1c, 0x22, 0x0b, 0x54, 0x0a, 0x54,
        0x09, 0x50, 0x53, 0x15, 0x1e, 0x38, 0x01, 0x0b, 0x53, 0x51,
        0x38, 0x04, 0x0f, 0x54, 0x04, 0x0c, 0x02, 0x15, 0x38, 0x5f,
        0x57, 0x54, 0x56, 0x55, 0x51, 0x52, 0x03, 0x1a
    ]
    
    # Create symbolic variables for each character in the flag
    flag = [BitVec(f'char_{i}', 8) for i in range(len(encrypted))]
    
    # Add constraints for each character
    for i in range(len(encrypted)):
        # The decryption operation: encrypted[i] ^ 0x67 == flag[i]
        s.add(encrypted[i] ^ 0x67 == flag[i])
        
        # Additional constraints for printable ASCII characters
        s.add(flag[i] >= 32)  # Space
        s.add(flag[i] <= 126) # Tilde
    
    # Check if the problem is satisfiable
    if s.check() == sat:
        model = s.model()
        # Reconstruct the flag from the model
        solution = ''.join([chr(model[flag[i]].as_long()) for i in range(len(flag))])
        print(f"Found valid flag: {solution}")
    else:
        print("No solution found")

if __name__ == "__main__":
    solve_flag()