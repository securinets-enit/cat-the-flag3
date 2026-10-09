#include <fcntl.h>
#include <stdio.h>
#include <unistd.h>

#define ANSWER_SIZE 64
#define INPUT_SIZE 256

__attribute__((noinline, force_align_arg_pointer))
void win(void)
{
    char flag[256];
    int fd = open("/flag", O_RDONLY);

    if (fd < 0) {
        fd = open("flag.txt", O_RDONLY);
    }

    if (fd < 0) {
        puts("The reward was returned to administration. Naturally.");
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
static void orientation(void)
{
    char answer[ANSWER_SIZE];

    puts("Jujutsu High guarantees that every student returns safely.");
    printf("Graduation statement: ");
    read(STDIN_FILENO, answer, INPUT_SIZE);
    puts("Statement filed. Your return destination has been selected.");
}

int main(void)
{
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);
    alarm(30);

    puts("=== JUJUTSU HIGH RETURN OFFICE ===");
    orientation();
    return 0;
}
