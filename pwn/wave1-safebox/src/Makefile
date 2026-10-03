CC = gcc
CFLAGS = -fno-stack-protector -no-pie -O0

all: safebox

safebox: safebox.c
	$(CC) $(CFLAGS) -o safebox safebox.c

clean:
	rm -f safebox
