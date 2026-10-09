#define _GNU_SOURCE

#include <errno.h>
#include <fcntl.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

#define MAX_PAYLOAD 512

__attribute__((noinline, used))
static void win(void)
{
    char flag[128];
    int fd = open("/flag", O_RDONLY);

    if (fd < 0) {
        _exit(1);
    }

    ssize_t length = read(fd, flag, sizeof(flag));

    if (length > 0) {
        write(STDOUT_FILENO, flag, (size_t)length);
    }

    _exit(0);
}

static int read_exact(unsigned char *buffer, size_t length)
{
    size_t received = 0;

    while (received < length) {
        ssize_t result = read(STDIN_FILENO, buffer + received, length - received);

        if (result == 0) {
            return -1;
        }

        if (result < 0) {
            if (errno == EINTR) {
                continue;
            }

            return -1;
        }

        received += (size_t)result;
    }

    return 0;
}

static size_t receive_technique(unsigned char *technique)
{
    char line[32];
    char *end;

    fputs("Length: ", stdout);

    if (fgets(line, sizeof(line), stdin) == NULL) {
        _exit(0);
    }

    errno = 0;
    unsigned long length = strtoul(line, &end, 10);

    if (errno != 0 || end == line || (*end != '\n' && *end != '\0') ||
        length == 0 || length > MAX_PAYLOAD) {
        puts("Rejected.");
        _exit(1);
    }

    fputs("Technique: ", stdout);

    if (read_exact(technique, (size_t)length) < 0) {
        _exit(1);
    }

    for (size_t left = 0, right = (size_t)length - 1; left < right; left++, right--) {
        unsigned char byte = technique[left];
        technique[left] = technique[right];
        technique[right] = byte;
    }

    technique[length] = '\0';
    return (size_t)length;
}

__attribute__((noinline))
static void inspection(void)
{
    unsigned char technique[MAX_PAYLOAD + 1];

    for (int round = 1; round <= 2; round++) {
        printf("\nInspection %d/2\n", round);
        receive_technique(technique);
        fputs("Verdict: ", stdout);
        printf((char *)technique);
        putchar('\n');
    }

    puts("Certified harmless.");
}

int main(void)
{
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);
    alarm(30);

    puts("=== JUJUTSU HIGH TECHNIQUE REVIEW ===");
    puts("Two inspections. Zero possible mistakes.");
    inspection();
    return 0;
}
