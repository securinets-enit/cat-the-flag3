#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

void init_buffering(void) {
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stderr, NULL, _IONBF, 0);
}

void secret_jackpot(void) {
    char flag[128];
    FILE *f = fopen("flag.txt", "r");
    if (!f) {
        puts("[-] flag.txt missing! Contact organizers.");
        exit(1);
    }
    if (fgets(flag, sizeof(flag), f)) {
        printf("\n[+] JACKPOT! You beat the house!\n");
        printf("[+] Flag: %s\n", flag);
    }
    fclose(f);
}

// Memory layout in play():
// char buffer[40];
// volatile int lucky_target;
// Off-by-one: loop condition (i <= 40) writes 41 bytes into buffer[40].
// The 41st byte directly overwrites the least significant byte of lucky_target.
int play(void) {
    char buffer[40];
    volatile int lucky_target = 0;

    puts("Place your bet on the table (max 40 characters):");
    for (int i = 0; i <= 40; i++) {
        char c;
        if (read(0, &c, 1) != 1) break;
        if (c == '\n') break;
        buffer[i] = c;
    }

    return lucky_target;
}

int main(void) {
    init_buffering();
    puts("==================================================");
    puts("    SecurinetsENIT CTF - Flag Roulette v1.0       ");
    puts("==================================================");
    puts("Welcome to high-stakes roulette.");

    int result = play();
    // Requires the least significant byte to be 0x77 ('w')
    if ((result & 0xFF) == 0x77) {
        secret_jackpot();
    } else {
        printf("[-] House wins! Result token: 0x%08x\n", result);
        puts("[-] Hint: An off-by-one index can flip your luck!");
    }

    return 0;
}
