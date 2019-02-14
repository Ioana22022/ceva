extern puts
 
global main
 
section .data
  callDenied: db 'call denied!',0x0a,0
  nothingToCall: db 'nothing to call!',0x0a,0
  noPoint: db 'Should not start with point!!',0x0a,0
section .text
main:
  push ebp
  mov ebp, esp
 
check_argc:
 mov eax, [ebp + 8] ; this is where argc sits
 cmp eax, 1
 jg check_argv1 ;it's ok
 push nothingToCall
 call puts
 jmp done

check_argv1:
  mov eax, [ebp + 12] ; accessing argv
  add eax, 4 ; accesing argv + 1
  mov eax, [eax] ; dereference argv + 1
  mov dl, byte [eax]
  cmp dl, 46 ; 0x2E == 46 equivalent to point
  jne do_execve ; it's ok
  push noPoint
  call puts
  jmp done
  
do_execve:
; syscall number
  mov eax, 11

; load argv[1] into ebx
  mov ebx, [ebp + 12]
  add ebx, 4
  mov ebx, [ebx]

; load &argv[1] into ecx
  mov edx, [ebp + 12]
  lea ecx, [edx + 4]

; env into edx --> set to 0
  and edx, 0

; set interrupt
  int 0x80 
  jmp done

done:
  leave
  ret
