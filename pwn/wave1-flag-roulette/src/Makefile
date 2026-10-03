CC = gcc
CFLAGS = -fno-stack-protector -no-pie -O0

all: flag_roulette

flag_roulette: flag_roulette.c
	$(CC) $(CFLAGS) -o flag_roulette flag_roulette.c

clean:
	rm -f flag_roulette
