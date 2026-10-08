#include <fcntl.h>
#include <inttypes.h>
#include <stdint.h>
#include <stdio.h>
#include <unistd.h>

#define BALANCE UINT32_C(100)
#define PRICE UINT32_C(65536)
#define MINIMUM_ORDER UINT32_C(65536)

static void reveal_receipt(void)
{
    char receipt[256];
    int fd = open("/flag", O_RDONLY);

    if (fd < 0) {
        fd = open("flag.txt", O_RDONLY);
    }

    if (fd < 0) {
        puts("The receipt vanished. Management blames a curse, obviously.");
        return;
    }

    ssize_t length = read(fd, receipt, sizeof(receipt));
    close(fd);

    if (length <= 0) {
        puts("Your receipt is empty. Somehow that still matches your balance.");
        return;
    }

    fwrite(receipt, 1, (size_t)length, stdout);

    if (receipt[length - 1] != '\n') {
        putchar('\n');
    }
}

int main(void)
{
    uint32_t quantity;

    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);

    puts("=== JUJUTSU HIGH BLACK FLASH ===");
    puts("Only financially gifted sorcerers should continue.");
    printf("Your balance: %" PRIu32 " cursed credits\n", BALANCE);
    printf("Price per cursed tool: %" PRIu32 " cursed credits\n", PRICE);
    printf("Minimum wholesale order: %" PRIu32 " tools\n", MINIMUM_ORDER);
    printf("Quantity: ");

    if (scanf("%" SCNu32, &quantity) != 1) {
        puts("That is not a quantity. Grade 4 mathematics strikes again.");
        return 1;
    }

    if (quantity < MINIMUM_ORDER) {
        puts("Rejected. Wholesale means wholesale, bargain sorcerer.");
        return 0;
    }

    uint32_t total = quantity * PRICE;

    printf("Calculated total: %" PRIu32 " cursed credits\n", total);

    if (total > BALANCE) {
        puts("Insufficient funds. Try inheriting a better technique.");
        return 0;
    }

    puts("Payment approved. Accounting remains undefeated.");
    reveal_receipt();
    return 0;
}
