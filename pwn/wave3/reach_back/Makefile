CC ?= gcc
AS ?= as
LD ?= ld

CFLAGS := -O2 -Wall -Wextra -Wpedantic -Werror -fno-stack-protector
LDFLAGS := -Wl,-z,relro,-z,now,-z,noexecstack

.PHONY: all clean solver run docker test

all: harness

harness: harness.o caller.o
	$(CC) $(LDFLAGS) -o $@ $^ -ldl

harness.o: harness.c
	$(CC) $(CFLAGS) -c -o $@ $<

caller.o: caller.S
	$(CC) -c -o $@ $<

solve.o: solve.s
	$(AS) -o $@ $<

solve.so: solve.o
	$(LD) -shared -z noexecstack -o $@ $<

solver: solve.so

test: all solver
	./harness ./solve.so | grep -aFf flag >/dev/null
	@echo "Local harness test passed."

run: all
	socat TCP-LISTEN:8001,reuseaddr,fork,max-children=32 EXEC:'timeout 12s /usr/bin/python3 ./server.py',stderr

docker:
	docker compose up --build -d

clean:
	rm -f harness harness.o caller.o solve.o solve.so
