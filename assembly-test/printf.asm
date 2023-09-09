section .data
    format db "Hello World!", 0    ; Null-terminated format string

section .text
    global main

main:
    ; Prepare the arguments to printf
    push format

    ; Call printf
    call printf

    ; Clean up the stack
    add esp, 4  ; Assuming 4 bytes were pushed

    ; Exit the program
    mov eax, 1  ; syscall number for exit
    xor ebx, ebx  ; exit status: 0
    int 0x80  ; Invoke the syscall

extern printf   ; Declare printf as an external C function
