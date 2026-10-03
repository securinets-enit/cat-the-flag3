CC = gcc
CFLAGS = -fno-stack-protector -no-pie -O0

all: jumpstart

jumpstart: jumpstart.c
	$(CC) $(CFLAGS) -o jumpstart jumpstart.c

clean:
	rm -f jumpstart
