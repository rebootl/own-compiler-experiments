global _start

section .text

exit:
  mov ebx, eax
  mov eax, 1
  int 0x80

printchar:
  push ebp            ; save base pointer
  mov ebp, esp        ; set base pointer

  mov ecx, ebp   ;
  add ecx, 8;
  ;push 65
  ;push ebp + 8

  mov eax, 4          ; write
  mov ebx, 1          ; stdout
  ;mov ecx, esp
  mov edx, 1          ; length
  int 0x80

  mov esp, ebp
  pop ebp
  ret

print:  ; print eax as decimal
        ; eax is input

  mov ecx, 10 ; digit count to generate
              ; 32-bit max = 4,294,967,295
              ; -> max 10 digits
print_loop1:
    ; we divide by 10 to get the digits
    ; convert the remainder to ascii
    ; and push it to the stack
  call   print_divideby10
  add    eax, 0x30
  push   eax
  mov    eax, edx
  dec    ecx
  jne    print_loop1

  mov    ecx, 10          ; digit count to print
print_loop2:
  pop    eax
  call   printchar
  dec    ecx
  jne    print_loop2
  ret
print_divideby10:     ; divide eax by 10
                      ; eax is input, eax is output
                  ; edx is output remainder
  mov    ebx, 10
  xor    edx, edx
  div    ebx
  ret

_start:
  mov eax, 4
  inc eax
  inc eax
  mov eax, 5
  jmp print
  mov eax, 10
  jmp exit
