all: execve math libfunny.so

execve: execve.asm
	nasm -f elf32 execve.asm
	gcc -lc -m32 execve.o -o execve

math: math.asm
	nasm -f elf32 math.asm
	gcc -lc -m32 math.o -o math

libfunny.so: libfunny.asm
	nasm -f elf32 libfunny.asm
	ld -shared -lc -m elf_i386 libfunny.o -o libfunny.so

.PHONY: clean

clean:
	rm -f execve execve.o math math.o libfunny.o libfunny.so
