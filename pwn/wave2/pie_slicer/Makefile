CC = gcc
CFLAGS = -fno-stack-protector -fPIE -pie -O0

all: pie_slicer

pie_slicer: pie_slicer.c
	$(CC) $(CFLAGS) -o pie_slicer pie_slicer.c

clean:
	rm -f pie_slicer
