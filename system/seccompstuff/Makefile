CC=gcc
CFLAGS=

.PHONY: clean all

all: nonetwork
clean:
	rm -f nonetwork

nonetwork: nonetwork.c
	$(CC) $(CFLAGS) nonetwork.c -o nonetwork -lseccomp
