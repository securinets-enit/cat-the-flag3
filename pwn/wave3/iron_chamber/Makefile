CC = gcc
CFLAGS = -no-pie -z execstack -O0

all: iron_chamber

iron_chamber: iron_chamber.c
	$(CC) $(CFLAGS) -o iron_chamber iron_chamber.c

clean:
	rm -f iron_chamber
