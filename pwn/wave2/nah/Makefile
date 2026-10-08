CC = gcc
CFLAGS = -std=c11 -O2 -Wall -Wextra -Wpedantic -fstack-protector-strong -D_FORTIFY_SOURCE=2 -fPIE
LDFLAGS = -pie -Wl,-z,relro,-z,now

.PHONY: all solve clean

all: main

main: main.c
	$(CC) $(CFLAGS) -o $@ $< $(LDFLAGS)

solve: main
	python3 solver.py

clean:
	rm -f main
