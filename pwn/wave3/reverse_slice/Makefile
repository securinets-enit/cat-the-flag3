CC = gcc
CFLAGS = -std=gnu11 -O0 -Wall -Wextra -fstack-protector-all -fPIE -fno-omit-frame-pointer -fcf-protection=none
LDFLAGS = -pie -Wl,-z,relro,-z,now -Wl,-z,noexecstack

.PHONY: all solve clean

all: main

main: main.c
	$(CC) $(CFLAGS) -o $@ $< $(LDFLAGS)

solve: main
	python3 solver.py

clean:
	rm -f main
