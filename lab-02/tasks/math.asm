extern puts

global main

section .data
	thisistest: db 'this is a test',0x0a,0

section .text

main:
	push ebp
	mov ebp, esp
	sub esp, 32

	mov dword [ebp - 19], 1936287860
        mov dword [ebp - 15], 544434464
        mov dword [ebp - 11], 1702109281
        mov dword [ebp - 7], 29811
        mov byte  [ebp - 5], 0		; string terminator
        mov byte  [ebp - 4], 0		; i = 0
	jmp check_index

inside_loop:
	lea edx, [ebp - 19]		; edx = a
	mov eax, [ebp - 4]		; eax = i
	add eax, edx			; eax = a + i

	mov al, [eax]			; eax = a[i]

	mov bl, al			; save character
	xor eax, eax			; clear eax
	mov al, bl			; recover character

	imul eax, eax, 14		; eax = a[i] * 14
	lea ecx, [eax + 13]		; ecx = a[i] * 14 + 13

	mov eax, ecx			
	xor edx, edx

	mov ebx, 94
	div ebx				; remainder stored in dx
	
	xor ecx, ecx			; clear ecx
	mov cx, dx			; store remainder to cx
	add ecx, 33			; add 33 to it

	lea edx, [ebp - 19]		
	mov eax, [ebp - 4]
	add eax, edx
	mov byte [eax], cl

	add byte [ebp - 4], 1		; i = i + 1

check_index:
	cmp byte [ebp - 4], 13
	jg print_it
	jmp inside_loop

print_it:
	sub esp, 12
	lea eax, [ebp - 19]
	push eax
	call puts
	add esp, 16
	jmp done


done:
	leave
	ret


