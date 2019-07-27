##
#From inspecting the file with radare, we simply have to notice the parameters read() is called with, when being placed on the stack.
#After the open call, the return value is placed on eax, and then at [esp + 0x1c]. This is the file descriptor, which is the last one on the stack, 
#because the parameters will be placed on the stack for the read call in reverse order. Then comes the second parameter, which we will have to inspect. 
#That will be the pointer to the buffer where the number is stored.

#lea eax, dword [esp + 0x18] ; 24
#mov dword [esp + 4], eax

#So we see that the second parameter is placed at esp+0x4. Then, if using gdb with peda, it will show the number at which the address points to in hex form.
#After that, hit continue in gdb and place the number in decimal form, so it will later be passed to scanf.

#"You guessed it" should be printed.
