CC = gcc
CFLAGS = -fno-stack-protector -no-pie -z execstack -O0

TARGET = chall

.PHONY: all clean

all: $(TARGET)

$(TARGET): challenge.c
	@mkdir -p dist
	$(CC) $(CFLAGS) -o $(TARGET) challenge.c

clean:
	rm -f $(TARGET)