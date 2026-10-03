CC = gcc
CFLAGS = -fno-stack-protector -no-pie -O0

all: libc_voyage

libc_voyage: libc_voyage.c
	$(CC) $(CFLAGS) -o libc_voyage libc_voyage.c

clean:
	rm -f libc_voyage
