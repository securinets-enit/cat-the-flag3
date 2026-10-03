#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

void init_buffering(void) {
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stderr, NULL, _IONBF, 0);
}

void win(void) {
    // IMPORTANT: System V AMD64 ABI 16-byte alignment rule:
    // Calling system() invokes do_system in glibc.
    // Glibc uses SSE instructions:
    // movaps XMMWORD PTR [rsp + ...], xmm0
    // If RSP is not aligned to a 16-byte boundary (RSP % 16 == 0),
    // the CPU throws a General Protection Fault (SIGSEGV)!
    // To solve: prepend a 'ret' gadget or jump to win + 1 / win + 5.
    system("cat flag.txt");
}

void vuln(void) {
    char buffer[64];
    puts("Enter navigation telemetry data:");
    // Reads up to 128 bytes into a 64-byte buffer
    read(0, buffer, 128);
}

int main(void) {
    init_buffering();
    puts("==================================================");
    puts("       SecurinetsENIT CTF - Jumpstart v1.0        ");
    puts("==================================================");
    puts("Welcome, pilot. Coordinates locked.");
    vuln();
    puts("Telemetry confirmed. Returning to orbit.");
    return 0;
}
