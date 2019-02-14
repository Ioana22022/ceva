extern _GLOBAL_OFFSET_TABLE_
extern puts
 
; export a library function and a global var
global count_param:data 4
global leet_write:function
 
section .data
  leet: db "executing leet_write()", 0
  count_param: dd 0
 
section .text
leet_write:
  ; debugging purpose
  push leet
  call puts
 
  ; write your code here --------------------------------------------
  ; TODO
  ; -----------------------------------------------------------------
 
  add esp, 4 ; leet from above
  ret
