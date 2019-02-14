extern puts
section .data
	helloStr: db 'Hello world!',0
section .text
	global main
main:
	push helloStr
	call puts
