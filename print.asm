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

dividebyten:      ; divide eax by 10
                  ; eax is input, eax is output
                  ; edx is output remainder
  mov    ebx, 10
  mov    edx, 0       ; clear edx
  div    ebx          ; EDX:EAX / EBX = EAX remainder EDX
  ret

_start:

  ;mov eax, 1       ; char to print
  ;add eax, 0x30    ; convert to ascii
  ;push eax           ; push char
  ;call printchar      ; call printchar
  ;add esp, 4          ; pop char


  mov eax, 123        ; number to print

print_int:              ; print integer as decimal
                        ; eax is input
                        ; ecx is digit count
                        ; edx is remainder

  push   eax            ; save eax
  mov    ecx, 1
  cmp    eax, 0         ; check if digit count is zero
  je     print_int_loop2
  pop    eax            ; restore eax

  mov    ecx, 10        ; digit count to produce
                        ; 10 digits in a 32 bit integer
                        ; max 4'294'967'295
print_int_loop:

  call   dividebyten
  ;add    edx, 0x30      ; convert remainder to ascii
  push   edx            ; push digit

  dec    ecx             ; decrement digit count
  jne    print_int_loop  ; loop until digit count is zero

  mov    ecx, 10         ; digit count to print
print_remove_leading_zeroes:
  pop    eax
                        ; check if digit is zero
                        ; if so, don't print
  ;mov    ebx, eax
  ;sub    ebx, 0x30      ; convert ascii to digit
  dec    ecx
  cmp    eax, 0
  je    print_remove_leading_zeroes
  inc    ecx
  push   eax            ; push digit back on stack

print_int_loop2:
  pop    eax
  add    eax, 0x30      ; convert remainder to ascii
                        ; call routine
  push   ecx            ; save digit count
  push   eax            ; push ascii digit
  call   printchar
  add    esp, 4         ; clear stack
  pop    ecx            ; restore digit count

  dec    ecx
  jne    print_int_loop2

  ;exit
  mov eax, 0
  jmp exit
