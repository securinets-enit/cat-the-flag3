#include <fcntl.h>
#include <limits.h>
#include <stdint.h>
#include <stdio.h>
#include <unistd.h>

#define MAX_CURSES 253

static int curse_fds[MAX_CURSES];
static size_t curse_count;
static uint8_t protected_fd;
static int special_grade_loaded;

static void menu(void)
{
    puts("\n=== JUJUTSU HIGH CURSED VAULT ===");
    puts("1. Register a low-grade cursed object");
    puts("2. Seal the special-grade object");
    puts("3. Request a cursed object");
    puts("4. Run before Gojo notices");
    printf("> ");
}

static void register_curse(void)
{
    if (special_grade_loaded) {
        puts("The vault is sealed. Planning ahead was apparently too advanced.");
        return;
    }

    if (curse_count >= MAX_CURSES) {
        puts("The vault is full. Even your bad ideas need storage limits.");
        return;
    }

    int fd = open("/dev/null", O_RDONLY);

    if (fd < 0) {
        puts("Registration failed. The curse showed better judgment than you.");
        return;
    }

    curse_fds[curse_count++] = fd;
    puts("Another Grade 4 curse registered. Terrifying.");
}

static void seal_special_grade(void)
{
    if (special_grade_loaded) {
        puts("It is already sealed. Try keeping up.");
        return;
    }

    int real_fd = open("/flag", O_RDONLY);

    if (real_fd < 0) {
        real_fd = open("flag.txt", O_RDONLY);
    }

    if (real_fd < 0) {
        puts("The special-grade object escaped. Excellent work.");
        return;
    }

    protected_fd = (uint8_t)real_fd;
    special_grade_loaded = 1;
    puts("Special-grade object sealed. Nothing can possibly go wrong.");
}

static void request_object(void)
{
    unsigned int requested_fd;
    char object[256];

    if (!special_grade_loaded) {
        puts("There is nothing special to request. Much like your technique.");
        return;
    }

    printf("Object descriptor: ");

    if (scanf("%u", &requested_fd) != 1 || requested_fd > INT_MAX) {
        puts("Invalid descriptor. Even Yuji understood the form.");
        return;
    }

    if (requested_fd == protected_fd) {
        puts("Access denied. Asking nicely is not a cursed technique.");
        return;
    }

    ssize_t length = read((int)requested_fd, object, sizeof(object));

    if (length <= 0) {
        puts("Nothing came back. A result worthy of your rank.");
        return;
    }

    puts("Barrier bypassed. The higher-ups will call this an isolated incident.");
    fwrite(object, 1, (size_t)length, stdout);

    if (object[length - 1] != '\n') {
        putchar('\n');
    }
}

int main(void)
{
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);

    for (int fd = 3; fd < 1024; fd++) {
        close(fd);
    }

    puts("Jujutsu High guarantees this barrier is completely flawless.");

    while (1) {
        unsigned int choice;

        menu();

        if (scanf("%u", &choice) != 1) {
            break;
        }

        if (choice == 1) {
            register_curse();
        } else if (choice == 2) {
            seal_special_grade();
        } else if (choice == 3) {
            request_object();
        } else if (choice == 4) {
            puts("Gojo noticed. Try looking innocent.");
            break;
        } else {
            puts("Invalid choice. The menu has defeated another sorcerer.");
        }
    }

    return 0;
}
