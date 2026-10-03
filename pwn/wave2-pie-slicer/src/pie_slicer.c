#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

void init_buffering(void) {
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stderr, NULL, _IONBF, 0);
}

void win(void) {
    char flag[128];
    FILE *f = fopen("flag.txt", "r");
    if (!f) {
        puts("[-] flag.txt missing! Contact organizers.");
        exit(1);
    }
    if (fgets(flag, sizeof(flag), f)) {
        printf("\n[+] SUCCESS! Sliced right through PIE!\n");
        printf("[+] Flag: %s\n", flag);
    }
    fclose(f);
}

void slice(void) {
    char buffer[64];
    puts("How precisely can you slice the pie?");
    printf("Provide your slice parameters: ");
    
    // 64 bytes buffer + 8 bytes saved RBP = 72 bytes.
    // 74 bytes allows overwriting exactly the lowest 2 bytes of Saved RIP!
    ssize_t n = read(0, buffer, 74);
    if (n <= 0) {
        puts("[-] No input.");
        return;
    }
    puts("[+] Slice received.");
}

int main(void) {
    init_buffering();
    puts("==================================================");
    puts("       SecurinetsENIT CTF - PIE Slicer v1.0       ");
    puts("==================================================");
    puts("PIE (Position Independent Executable) is fully enabled.");
    puts("Can you navigate memory when the base is unknown?\n");

    slice();

    puts("Leaving bakery. Goodbye!");
    return 0;
}
