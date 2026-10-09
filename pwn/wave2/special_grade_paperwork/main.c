#define _GNU_SOURCE

#include <errno.h>
#include <stdio.h>
#include <unistd.h>

#define DRAFT_SIZE 64
#define PREVIEW_SIZE 80
#define FINAL_SIZE 256

__asm__(
    ".global pop_rdi_ret\n"
    "pop_rdi_ret:\n"
    "pop %rdi\n"
    "ret\n"
    ".global plain_ret\n"
    "plain_ret:\n"
    "ret\n"
);

static int read_fully(void *buffer, size_t length)
{
    size_t received = 0;

    while (received < length) {
        ssize_t result = read(STDIN_FILENO, (char *)buffer + received, length - received);

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

__attribute__((noinline))
static void audit(void)
{
    char report[DRAFT_SIZE];

    puts("\nInitial submission: exactly 64 bytes.");
    fputs("Draft: ", stdout);

    if (read_fully(report, sizeof(report)) < 0) {
        _exit(0);
    }

    puts("Committee preview:");

    if (write(STDOUT_FILENO, report, PREVIEW_SIZE) != PREVIEW_SIZE) {
        _exit(1);
    }

    putchar('\n');
    fputs("Final copy: ", stdout);

    if (read(STDIN_FILENO, report, FINAL_SIZE) <= 0) {
        _exit(0);
    }

    puts("Filed.");
}

int main(void)
{
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);
    alarm(30);

    puts("=== JUJUTSU HIGH SECURITY COMMITTEE ===");
    puts("Special-grade paperwork. Intern-grade review.");
    audit();
    return 0;
}
