#include <stdio.h>
#include <stdlib.h>
#include <string.h>
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
        printf("\n[+] REVELATION! The Oracle surrenders the secret!\n");
        printf("[+] Flag: %s\n", flag);
    }
    fclose(f);
    exit(0);
}

void oracle_loop(void) {
    char buffer[128];
    while (1) {
        memset(buffer, 0, sizeof(buffer));
        puts("\nConsult the Oracle (type 'exit' to depart):");
        if (!fgets(buffer, sizeof(buffer), stdin)) break;
        if (strncmp(buffer, "exit", 4) == 0) {
            puts("The Oracle closes the veil. Farewell.");
            exit(0);
        }
        printf("The Oracle speaks: ");
        // Format string vulnerability: user input directly evaluated
        printf(buffer);
    }
}

int main(void) {
    init_buffering();
    puts("==================================================");
    puts("     SecurinetsENIT CTF - Format Oracle v1.0      ");
    puts("==================================================");
    puts("Welcome, seeker of hidden knowledge.");
    oracle_loop();
    return 0;
}
