global main

section .text
main:
  mov eax, 4
  inc eax
  inc eax
  mov eax, 5

  mov ecx, eax
  mov eax, 4 ; write
  mov ebx, 1 ; stdout
	mov	ecx, msg
	mov	edx, msg.len
  int 0x80

  mov eax, 10
  jmp exit
  mov eax, 0  ; default
exit:
  mov ebx, eax
  mov eax, 1
  int 0x80

section .data
msg:	db	"Hello, world!", 10
.len:	equ	$ - msg
