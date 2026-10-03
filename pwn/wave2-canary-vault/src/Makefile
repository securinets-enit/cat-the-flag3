CC = gcc
CFLAGS = -fstack-protector-all -no-pie -O0

all: canary_vault

canary_vault: canary_vault.c
	$(CC) $(CFLAGS) -o canary_vault canary_vault.c

clean:
	rm -f canary_vault
