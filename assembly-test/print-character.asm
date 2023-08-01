global _start

section .text

exit:
  mov ebx, eax
  mov eax, 1
  int 0x80

printchar:
  push ebp            ; save base pointer
  mov ebp, esp        ; set base pointer
                      ; this clears the stack
                      ; and creates a new stack frame

  mov ecx, ebp        ; set ecx to base pointer
  add ecx, 8          ; 8 bytes from base pointer
                      ; this is the first argument

  mov eax, 4          ; write
  mov ebx, 1          ; stdout
                      ; ecx already set
  mov edx, 1          ; length
  int 0x80

  mov esp, ebp
  pop ebp
  ret


_start:

  push 'A'            ; push char
  call printchar      ; call printchar
  add esp, 4          ; pop char

  mov eax, 12
  jmp exit
