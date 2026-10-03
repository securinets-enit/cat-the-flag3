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
        printf("\n[+] SUCCESS! Canary bypassed and control seized!\n");
        printf("[+] Flag: %s\n", flag);
    }
    fclose(f);
}

void stage1_leak(void) {
    char name[32];
    memset(name, 0, sizeof(name));
    
    puts("Stage 1: Register your agent callsign:");
    // If player sends exactly 32 bytes without null termination,
    // the subsequent printf will print right into the stack canary!
    read(0, name, 32);
    printf("Agent registered: %s\n", name);
}

void stage2_overflow(void) {
    char response[64];
    puts("\nStage 2: Submit encrypted payload to vault:");
    // Bounded buffer overflow with stack protector active
    read(0, response, 128);
    puts("[+] Payload received. Verifying integrity...");
}

int main(void) {
    init_buffering();
    puts("==================================================");
    puts("     SecurinetsENIT CTF - Canary Vault v1.0       ");
    puts("==================================================");
    puts("Warning: Stack Canary protection (fs:0x28) is active.");
    puts("Any unauthorized memory corruption will terminate the process.\n");

    stage1_leak();
    stage2_overflow();

    puts("Vault session closed safely.");
    return 0;
}
