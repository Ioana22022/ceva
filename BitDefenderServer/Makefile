CC=gcc
CFLAGS=-Wall -pthread


all: server

server: server.c
	$(CC) $(CFLAGS) server.c -o $@ 

clean:
	rm -f server index.*
