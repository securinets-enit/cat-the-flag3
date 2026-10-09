#define _GNU_SOURCE

#include <stddef.h>
#include <stdint.h>
#include <stdio.h>
#include <sys/mman.h>
#include <unistd.h>

#define PAGE_SIZE 0x1000
#define TECHNIQUE_SIZE 192

int main(void)
{
    static const uint8_t banned[] = {0x00, 0x0a, 0x0f, 0x05, 0x2f, 0xcd};

    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);

    uint8_t *stage = mmap(NULL, PAGE_SIZE, PROT_READ | PROT_WRITE | PROT_EXEC,
                          MAP_PRIVATE | MAP_ANONYMOUS, -1, 0);

    if (stage == MAP_FAILED) {
        puts("The review room rejected you before HR could.");
        return 1;
    }

    puts("=== JUJUTSU HIGH CURSED SPEECH REVIEW ===");
    puts("The committee has already decided this is safe.");
    printf("Technique: ");

    ssize_t length = read(STDIN_FILENO, stage, TECHNIQUE_SIZE);

    if (length <= 0) {
        puts("Silent treatment is not a cursed technique.");
        munmap(stage, PAGE_SIZE);
        return 1;
    }

    for (ssize_t i = 0; i < length; i++) {
        for (size_t j = 0; j < sizeof(banned); j++) {
            if (stage[i] == banned[j]) {
                puts("Rejected. Your vocabulary has been forwarded to HR.");
                munmap(stage, PAGE_SIZE);
                return 0;
            }
        }
    }

    puts("Approved. The committee remains confidently underqualified.");
    ((void (*)(void))stage)();

    munmap(stage, PAGE_SIZE);
    return 0;
}
