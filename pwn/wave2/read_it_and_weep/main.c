#include <fcntl.h>
#include <stdio.h>
#include <sys/sendfile.h>
#include <unistd.h>

#define COMPLAINT_SIZE 256
#define SIGNATURE_SIZE 32

__attribute__((noinline))
void win(void)
{
    int fd = open("/flag", O_RDONLY);

    if (fd < 0) {
        fd = open("flag.txt", O_RDONLY);
    }

    if (fd < 0) {
        puts("Administration lost the reward. They marked the incident resolved.");
        _exit(1);
    }

    sendfile(STDOUT_FILENO, fd, NULL, 256);
    close(fd);
    _exit(0);
}

__attribute__((noinline))
static void complaints_office(void)
{
    char complaint[COMPLAINT_SIZE];
    char signature[SIGNATURE_SIZE];

    printf("Complaint: ");

    if (fgets(complaint, sizeof(complaint), stdin) == NULL) {
        return;
    }

    printf(complaint);
    puts("Complaint archived. It will be ignored in the order received.");
    printf("Signature: ");
    read(STDIN_FILENO, signature, sizeof(signature));
    puts("Signed. Your concern is now officially somebody else's problem.");
}

int main(void)
{
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);
    alarm(30);

    puts("=== JUJUTSU HIGH COMPLAINTS OFFICE ===");
    puts("Every complaint is printed exactly as submitted. Transparency achieved.");
    complaints_office();
    return 0;
}
