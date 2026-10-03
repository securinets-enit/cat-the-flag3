#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

void init_buffering(void) {
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stderr, NULL, _IONBF, 0);
}

// Built-in helper to provide authentic ROP gadgets in small ELF binaries
void gadget_store(void) {
    __asm__(
        "pop %rdi; ret;\n"
        "pop %rsi; pop %r15; ret;\n"
    );
}

void win(unsigned long long code1, unsigned long long code2) {
    if (code1 == 0x1337c0deULL && code2 == 0xcafebebeULL) {
        char flag[128];
        FILE *f = fopen("flag.txt", "r");
        if (!f) {
            puts("[-] flag.txt missing! Contact organizers.");
            exit(1);
        }
        if (fgets(flag, sizeof(flag), f)) {
            printf("\n[+] ACCESS GRANTED! Citadel gate unlocked.\n");
            printf("[+] Flag: %s\n", flag);
        }
        fclose(f);
    } else {
        puts("\n[-] ACCESS DENIED! Gate credentials invalid.");
        printf("[-] Received code1: 0x%llx (Expected: 0x1337c0de)\n", code1);
        printf("[-] Received code2: 0x%llx (Expected: 0xcafebebe)\n", code2);
    }
}

void challenge(void) {
    char buffer[80];
    puts("Present your authorization sequence to the Gatekeeper:");
    // Reads up to 160 bytes into an 80-byte buffer
    read(0, buffer, 160);
}

int main(void) {
    init_buffering();
    puts("==================================================");
    puts("      SecurinetsENIT CTF - Gatekeeper v1.0        ");
    puts("==================================================");
    puts("The Citadel gates are locked with dual-key cryptographic validation.");
    challenge();
    puts("Verification sequence completed. Gates remain sealed.");
    return 0;
}
