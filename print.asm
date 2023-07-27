global _start

section .text

exit:
  mov ebx, eax
  mov eax, 1
  int 0x80

printchar:
  ; Preserve the registers you want to use (eax, ebx, ecx)
  ;push eax
  ;push ebx
  ;push ecx
  ;push edx

  push ebp            ; save base pointer
  mov ebp, esp        ; set base pointer
                      ; this clears the stack
                      ; and creates a new stack frame

  mov ecx, ebp        ; set ecx to base pointer
  add ecx, 8         ; 8 bytes from base pointer
                      ; this is the first argument

  mov eax, 4          ; write
  mov ebx, 1          ; stdout
                      ; ecx already set
  mov edx, 1          ; length
  int 0x80

  mov esp, ebp
  pop ebp

  ; Restore the registers you used
  ;pop edx
  ;pop ecx
  ;pop ebx
  ;pop eax
  ret

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
  ;pop    eax
  call   printchar
  pop    eax
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

print:  ; print eax as decimal
        ; eax is input

  mov ecx, 10 ; digit count to generate
              ; 32-bit max = 4,294,967,295
              ; -> max 10 digits
  jmp print_loop1
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


  mov eax, 1234         ; number to print

  mov    ecx, 10        ;  digit count to produce
loop:
  call   dividebyten
  add    edx, 0x30      ; convert remainder to ascii

  push   eax            ; push result
  push   ecx            ; save digit count
  push   edx            ; push ascii digit
  call   printchar
  add    esp, 4         ; clear stack
  pop    ecx            ; restore digit count
  pop    eax            ; restore result

  dec    ecx             ; decrement digit count
  jne    loop


  ;exit
  mov eax, 0
  jmp exit
