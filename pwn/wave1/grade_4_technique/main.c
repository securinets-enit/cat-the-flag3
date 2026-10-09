#define _GNU_SOURCE

#include <stdio.h>
#include <sys/mman.h>
#include <unistd.h>

#define PAGE_SIZE 0x1000
#define TECHNIQUE_SIZE 256

int main(void)
{
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);

    void *stage = mmap(NULL, PAGE_SIZE, PROT_READ | PROT_WRITE | PROT_EXEC,
                       MAP_PRIVATE | MAP_ANONYMOUS, -1, 0);

    if (stage == MAP_FAILED) {
        puts("Even the arena rejected you.");
        return 1;
    }

    puts("=== JUJUTSU HIGH TECHNIQUE EXAM ===");
    puts("Grade 4 candidates get one generous attempt.");
    printf("Technique: ");

    ssize_t length = read(STDIN_FILENO, stage, TECHNIQUE_SIZE);

    if (length <= 0) {
        puts("Nothing? A bold interpretation of having a technique.");
        return 1;
    }

    puts("Evaluation begins. Expectations remain manageable.");
    ((void (*)(void))stage)();

    munmap(stage, PAGE_SIZE);
    return 0;
}
