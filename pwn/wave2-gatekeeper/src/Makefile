CC = gcc
CFLAGS = -fno-stack-protector -no-pie -O0

all: gatekeeper

gatekeeper: gatekeeper.c
	$(CC) $(CFLAGS) -o gatekeeper gatekeeper.c

clean:
	rm -f gatekeeper
