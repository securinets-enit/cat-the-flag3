CC ?= gcc

CFLAGS ?= -Wall -Wextra -O0 -g

# This challenge intentionally needs predictable code addresses and no stack
# canary. Keep the other default hardening provided by the toolchain enabled.
CHALLENGE_CFLAGS = -fno-stack-protector -fno-pie
CHALLENGE_LDFLAGS = -no-pie

SOURCES := $(wildcard *.c)
TARGETS := $(SOURCES:.c=)

.PHONY: all clean

all: $(TARGETS)

%: %.c
	$(CC) $(CFLAGS) $(CHALLENGE_CFLAGS) $< -o $@ $(CHALLENGE_LDFLAGS)

clean:
	$(RM) $(TARGETS)