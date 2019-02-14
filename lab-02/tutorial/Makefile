all: hello hello_min cdecl stdcall fastcall for while nested

hello: hello.c
	gcc -m32 -O0 $< -o $@

hello_min: hello.asm
	nasm -f elf32 hello.asm
	ld -s -lc -m elf_i386 -dynamic-linker /lib/ld-linux.so.2 -e main hello.o -o hello_min

cdecl: cdecl.c
	gcc -O0 -m32 $< -o $@

stdcall: stdcall.c
	gcc -O0 -m32 $< -o $@

fastcall: fastcall.c
	gcc -O0 -m32 $< -o $@

for: for.c
	gcc -O0 -std=c99 -m32 $< -o $@

while: while.c
	gcc -O0 -m32 $< -o $@

nested: nested.c
	gcc -O0 -m32 $< -o $@

.PHONY: clean

clean:
	rm -f hello hello.o hello_min cdecl stdcall fastcall for while nested
