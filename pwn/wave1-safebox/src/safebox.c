#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

void init_buffering(void) {
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stderr, NULL, _IONBF, 0);
}

// Memory Layout & Compiler Alignment:
// key_buffer: 28 bytes
// unsigned long long master_key: 8 bytes (requires 8-byte alignment on AMD64 ABI)
// Compiler adds 4 bytes of padding: 28 + 4 = 32 bytes (0x20) offset!
struct Vault {
    char key_buffer[28];
    unsigned long long master_key;
    int is_unlocked;
};

void win(void) {
    char flag[128];
    FILE *f = fopen("flag.txt", "r");
    if (!f) {
        puts("[-] flag.txt missing! Please contact organizers.");
        exit(1);
    }
    if (fgets(flag, sizeof(flag), f)) {
        printf("\n[+] Access Granted! Vault unlocked.\n");
        printf("[+] Flag: %s\n", flag);
    }
    fclose(f);
}

int main(void) {
    init_buffering();

    struct Vault vault;
    memset(&vault, 0, sizeof(vault));
    vault.master_key = 0x1122334455667788ULL;
    vault.is_unlocked = 0;

    puts("==================================================");
    puts("        SecurinetsENIT CTF - Safebox v1.0         ");
    puts("==================================================");
    puts("Welcome, operative.");
    puts("Our defense module holds the master vault key.");
    puts("Provide your passcode to authenticate.\n");

    printf("Enter passcode: ");
    ssize_t n = read(0, vault.key_buffer, 48);
    if (n <= 0) {
        puts("[-] No input received.");
        return 1;
    }

    // Expected master_key: 0x5345435552495445 ("SECURITE" in ASCII, little-endian)
    if (vault.master_key == 0x5345435552495445ULL) {
        vault.is_unlocked = 1;
        win();
    } else {
        puts("\n[-] ACCESS DENIED!");
        printf("[-] Received master_key: 0x%016llx\n", vault.master_key);
        puts("[-] Expected master_key: 0x5345435552495445 ('SECURITE')");
        puts("[-] Hint: Inspect struct padding and little-endian ordering in GDB!");
    }

    return 0;
}
