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


  mov eax, 4949         ; number to print

print_int:              ; print integer as decimal
                        ; eax is input
                        ; ecx is digit count
                        ; edx is remainder

  mov    ecx, 10        ;  digit count to produce
print_int_loop:
  call   dividebyten
  add    edx, 0x30      ; convert remainder to ascii
  push   edx            ; push ascii digit

  dec    ecx             ; decrement digit count
  jne    print_int_loop  ; loop until digit count is zero

  mov    ecx, 10         ; digit count to print
print_int_loop2:
  pop    eax
                        ; check if digit is zero
                        ; if so, don't print
  mov    ebx, eax
  sub    ebx, 0x30      ; convert ascii to digit
  cmp    ebx, 0
  je    print_int_decjump

                        ; call routine
  push   ecx            ; save digit count
  push   eax            ; push ascii digit
  call   printchar
  add    esp, 4         ; clear stack
  pop    ecx            ; restore digit count

print_int_decjump:
  dec    ecx
  jne    print_int_loop2

  ;exit
  mov eax, 0
  jmp exit
