CC = gcc
CFLAGS = -no-pie -Wl,-z,lazy -O0

all: format_oracle

format_oracle: format_oracle.c
	$(CC) $(CFLAGS) -o format_oracle format_oracle.c

clean:
	rm -f format_oracle
