#include <fcntl.h>
#include <stdint.h>
#include <stdio.h>
#include <unistd.h>

#define SPEECH_SIZE 64
#define INPUT_SIZE 256
#define APPROVED_ARGUMENT UINT64_C(0x1337c0decafebabe)

__asm__(
    ".global pop_rdi_ret\n"
    "pop_rdi_ret:\n"
    "pop %rdi\n"
    "ret\n"
);

__attribute__((noinline, force_align_arg_pointer))
void win(uint64_t argument)
{
    char flag[256];

    if (argument != APPROVED_ARGUMENT) {
        puts("Loud, confident, and completely wrong. A natural debater.");
        return;
    }

    int fd = open("/flag", O_RDONLY);

    if (fd < 0) {
        fd = open("flag.txt", O_RDONLY);
    }

    if (fd < 0) {
        puts("The judges misplaced your prize. Their technique is bureaucracy.");
        _exit(1);
    }

    ssize_t length = read(fd, flag, sizeof(flag));
    close(fd);

    if (length > 0) {
        write(STDOUT_FILENO, flag, (size_t)length);
    }

    _exit(0);
}

__attribute__((noinline))
static void debate(void)
{
    char speech[SPEECH_SIZE];

    puts("The committee accepts one perfectly constructed argument.");
    printf("Your argument: ");
    read(STDIN_FILENO, speech, INPUT_SIZE);
    puts("Compelling. Unfortunately, confidence is not an ABI.");
}

int main(void)
{
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);
    alarm(30);

    puts("=== JUJUTSU HIGH DEBATE CLUB ===");
    debate();
    return 0;
}
