CC = gcc
CFLAGS = -std=gnu11 -O0 -Wall -Wextra -Wpedantic -Wno-format-security -U_FORTIFY_SOURCE -fstack-protector-strong -fno-PIE -fno-omit-frame-pointer -fcf-protection=none
LDFLAGS = -no-pie -Wl,-z,relro -Wl,-z,lazy -Wl,-z,noexecstack

.PHONY: all solve clean

all: main

main: main.c
	$(CC) $(CFLAGS) -o $@ $< $(LDFLAGS)

solve: main
	python3 solver.py

clean:
	rm -f main
