#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

void init_buffering(void) {
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stderr, NULL, _IONBF, 0);
}

// Built-in helper to guarantee the presence of clean ROP gadgets
void gadget_anchor(void) {
    __asm__(
        "pop %rdi; ret;\n"
        "ret;\n"
    );
}

void voyage(void) {
    char ship_log[64];
    puts("Log your expedition coordinates:");
    // Bounded overflow: reads up to 160 bytes into 64-byte buffer
    read(0, ship_log, 160);
    puts("Coordinates received. Sailing onward!");
}

int main(void) {
    init_buffering();
    puts("==================================================");
    puts("     SecurinetsENIT CTF - Libc Voyage v1.0        ");
    puts("==================================================");
    puts("No victory function awaits in these uncharted waters.");
    puts("You must chart your own course through the standard C library.\n");

    voyage();

    puts("Voyage concluded safely.");
    return 0;
}
