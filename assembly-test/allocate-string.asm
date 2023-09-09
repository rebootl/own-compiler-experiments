extern malloc, free, printf, fflush, stdout, concat

global main

section .data
  string_1: db "Hello World!", 0

section .text
  string_2: db "Hello World!", 0

exit:
  mov ebx, eax
  mov eax, 1
  int 0x80

printchar:
  push ebp            ; save base pointer
  mov ebp, esp        ; set base pointer
  push ebx            ; save ebx

  mov ecx, ebp        ; set ecx to base pointer
  add ecx, 8          ; 8 bytes from base pointer
                      ; this is the first argument

  mov eax, 4          ; write
  mov ebx, 1          ; stdout
                      ; ecx already set
  mov edx, 1          ; length
  int 0x80

  pop ebx             ; restore ebx
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

print_int:            ; print unsigned 32 bit integer
                      ; as decimal, removes leading zeroes
                      ; 1st argument is value to print
  ; prologue
  push ebp            ; save base pointer
  mov ebp, esp        ; set base pointer

  mov eax, [ebp+8]     ; read 1sr argument

  ; hack to prevent segmentation fault when value is zero
  ; -> why is there a segmentation fault?
  push   eax            ; save eax
  mov    ecx, 1
  cmp    eax, 0         ; check if digit count is zero
  je     print_int_loop2
  ;pop    eax            ; restore eax -> not needed ?

  ; check 1st bit from left for sign
  ; if set, print minus sign
  mov    ebx, eax
  shr    ebx, 31        ; shift right 31 bits
  jz     print_digit_count ; skip if positive
  push   eax            ; save eax
  push 45               ; ascii minus sign
  call   printchar
  add    esp, 4         ; clear stack
  pop    eax            ; restore eax

  not    eax            ; negate eax
  inc    eax            ; add 1

print_digit_count:
  mov    ecx, 10        ; digit count to produce
                        ; 10 digits in a 32 bit integer
                        ; max 4'294'967'295
                        ; 2'147'483'647 for signed integer
                        ; -2'147'483'648 for signed integer
print_int_loop:
  call   dividebyten    ; divide binary by 10, digit is
                        ; remainder in edx rest in eax
                        ; (reversed order)
  push   edx            ; push digit

  dec    ecx             ; decrement digit count
  jne    print_int_loop  ; loop until digit count is zero

  mov    ecx, 10         ; digit count to print
print_int_remove_leading_zeroes:
  pop    eax
                        ; check if digit is zero
                        ; if so, don't print
  dec    ecx
  cmp    eax, 0
  je    print_int_remove_leading_zeroes
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

  ; epilogue
  mov esp, ebp
  pop ebp
  ret

print_string:
  push ebp            ; save base pointer
  mov ebp, esp        ; set base pointer

  mov ecx, [ebp + 8]    ; read 1st argument

print_string_loop:
  mov eax, [ecx]        ; read 1st argument
  cmp eax, 0          ; check for null terminator
  je print_string_end ; if null terminator, end
  push ecx            ; save ecx
  push eax            ; save eax
  call printchar      ; print byte
  add esp, 4          ; clear stack
  pop ecx             ; restore ecx
  add ecx, 1          ; increment pointer
  jmp print_string_loop

print_string_end:
  ; epilogue
  mov esp, ebp
  pop ebp
  ret

allocate_mem:
  ; prologue
  push ebp
  mov ebp, esp
  push ebx

  ; get arguments
  mov ecx, [ebp + 8]    ; read 1st argument

  ;push ecx             ; save eax
  ;call print_int       ; print integer
  ;add esp, 4           ; clear stack
  push ebp

  mov eax, 192    ; mmap2
  mov ebx, 0      ; addr = 0
  mov ecx, 4096   ; len = 4096
  mov edx, 7     ; prot = PROT_READ|PROT_WRITE|PROT_EXEC
  mov esi, $22    ; flags = MAP_PRIVATE|MAP_ANONYMOUS
  mov edi, -1     ; fd = -1
  mov ebp, 0     ; offset = 0
  int 0x80         ; make call

  pop ebp

  ;push eax             ; save eax
  ;call print_int       ; print integer
  ;add esp, 4           ; clear stack

  ;check eax for error
  cmp eax, -1
  je allocate_mem_error

  ; epilogue
  pop ebx
  mov esp, ebp
  pop ebp
  ret

allocate_mem_error:
  mov eax, 55
  int 0x80

allocate_string:
  ; prologue
  push ebp
  mov ebp, esp
  push ebx

  mov eax, [ebp + 8]    ; read 1st argument

  mov ecx, 0            ; clear eax
allocate_string_loop:
  mov bl, [eax]        ; read byte

  ;push dword [eax]             ; save eax
  ;call printchar       ; print byte
  ;add esp, 4           ; clear stack

  cmp bl, 0            ; check for null terminator
  je allocate_string_endloop ; if null terminator, end
  inc ecx               ; increment counter
  inc eax               ; increment pointer
  jmp allocate_string_loop

allocate_string_endloop:
  ;push ecx             ; save eax
  ;call print_int       ; print integer
  ;add esp, 4           ; clear stack

  inc ecx               ; increment counter for null terminator
  push ecx              ; push length
  call allocate_mem     ; allocate memory
  add esp, 4            ; clear stack

  push eax             ; save eax
  ;call print_int       ; print integer
  ;add esp, 4           ; clear stack
  ;mov ebx, eax          ; save pointer to allocated memory
  mov edx, [ebp + 8]    ; read 1st argument
  ;mov edx, ebx          ; save pointer to allocated memory
allocate_string_loop2:
  mov bl, [edx]         ; read byte
  cmp bl, 0             ; check for null terminator
  je allocate_string_end2 ; if null terminator, end
  mov [eax], bl         ; copy byte
  inc edx               ; increment pointer
  inc eax               ; increment pointer
  jmp allocate_string_loop2

allocate_string_end2:
  mov word [edx], 0         ; copy null terminator

  pop eax             ; restore eax

  ; epilogue
  pop ebx
  mov esp, ebp
  pop ebp
  ret

main:
  push ebp
  mov ebp, esp

  ;call block_0

;  ; push string reference
;  push string_1
;
;  ; print stack top
;  call print_string
;  add esp, 4      ; clear stack
;
;  ;push string_1
;  ;call print_string
;  ; push string reference
;
;  push string_1
;  call allocate_string
;
;  push eax
;  call print_string
;
;  add esp, 4      ; clear stack
;
;  push 20
;  call malloc
;  add esp, 4      ; clear stack
;
;  push eax
;  call print_int
;  add esp, 4      ; clear stack
;  push dword string_2
;  call printf
;  add esp, 4      ; clear stack
;
;  push dword string_1
;  call printf
;  add esp, 4      ; clear stack
;

  push dword string_1
  push dword string_2
  call concat
;  call strcat
  add esp, 8      ; clear stack

  push eax
  call print_string
  add esp, 4      ; clear stack

  ;push dword [stdout]
  ;call fflush
  ;add esp, 4      ; clear stack

  ; default exit
  mov eax, 0
  jmp exit
