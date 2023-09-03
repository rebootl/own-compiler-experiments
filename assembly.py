# assembly chunks
#
# 32-bit x86 nasm assembly
#

PUSH_RESULT = '''
  ; push result
  push eax
'''

LITERAL = '''
  ; get literal
  mov eax, {}
'''

GET_PARAMETER = '''
  ; get parameter
  mov eax, ebp
  mov eax, [eax + {0}]
'''

UPDATE_LOCAL_VARIABLE = '''
  ; set local variable
  pop eax
  mov [ebp - {0}], eax
'''

POP_LOCAL_VARIABLE = '''
  ; pop local variable
  pop eax
'''

GET_LOCAL_VARIABLE = '''
  ; get local variable
  mov eax, ebp
  mov eax, [eax - {0}]
'''

PRIMARIES = {
  'println': '''
  ; print newline
  push 10                       ; ascii newline
  call printchar
  add esp, 4                    ; clear stack
''',
  'exit': '''
  ; jump to exit
  pop eax
  jmp exit
''',
  'print': '''
  ; print stack top
  call print_int
  add esp, 4      ; clear stack
''',
  #'var': None,
  'set': UPDATE_LOCAL_VARIABLE,
  'inc': '''
  ; increment stack top
  pop eax
  inc eax
  mov [ebp - {0}], eax
''',
  'dec': '''
  ; decrement stack top
  pop eax
  dec eax
  mov [ebp - {0}], eax
''',
  'return': '''
  ; return
  ;pop eax                   ; why do we pop here??
  mov esp, ebp
  pop ebp
  ret
''',
#  'consume': '''
#  ; consume stack top
#  pop eax
#''',
}

UNARIES = {
  'neg': '''
  ; negate stack top
  pop eax
  not    eax            ; negate eax
  inc    eax            ; add 1
''',
}

BINARIES = {
  'add': '''
  ; add stack top
  pop ebx
  pop eax
  add eax, ebx
  ;push eax
''',
  'sub': '''
  ; subtract stack top
  pop ebx
  pop eax
  sub eax, ebx
  ;push eax
''',
  'mul': '''
  ; multiply stack top
  pop ebx
  pop eax
  imul eax, ebx
  ;push eax
''',
  'div': '''
  ; divide stack top
  pop ebx
  pop eax
  cdq
  idiv ebx
  ;push eax
''',
  'mod': '''
  ; modulus stack top
  pop ebx
  pop eax
  cdq
  idiv ebx
  mov eax, edx
''',
}

CHECK_OVERFLOW = '''
  ; check for overflow
  jo overflow_true_{0}
  jmp overflow_false_{0}
overflow_true_{0}:
  mov eax, 1
  jmp overflow_end_{0}
overflow_false_{0}:
  mov eax, 0
overflow_end_{0}:
'''

CMP_START = '''
  pop ebx
  pop eax
  cmp eax, ebx
'''

CMP_END = '''
  jmp cmp_false_{0}
cmp_true_{0}:
  mov eax, 1
  jmp cmp_end_{0}
cmp_false_{0}:
  mov eax, 0
cmp_end_{0}:
'''

COMPARISONS = {
  'eq': '''
  ; equal
''' + CMP_START + '''
  je cmp_true_{0}     ; jump if equal
''' + CMP_END,
  'ne': '''
  ; not equal
''' + CMP_START + '''
  jne cmp_true_{0}     ; jump if not equal
''' + CMP_END,
  'gt': '''
  ; greater than
''' + CMP_START + '''
  jg cmp_true_{0}     ; jump if greater than
''' + CMP_END,
  'lt': '''
  ; less than
''' + CMP_START + '''
  jl cmp_true_{0}     ; jump if less than
''' + CMP_END,
  'ge': '''
  ; greater than or equal
''' + CMP_START + '''
  jge cmp_true_{0}     ; jump if greater than or equal
''' + CMP_END,
  'le': '''
  ; less than or equal
''' + CMP_START + '''
  jle cmp_true_{0}     ; jump if less than or equal
''' + CMP_END,
}

LOGICALS = {
  'and': '''
  ; logical and
  pop ebx
  pop eax
  cmp eax, 0
  jne a_true_{0}
  jmp r_false_{0}
a_true_{0}:
  cmp ebx, 0
  jne r_true_{0}
  jmp r_false_{0}
r_true_{0}:
  mov eax, 1
  jmp r_end_{0}
r_false_{0}:
  mov eax, 0
r_end_{0}:
''',
  'or': '''
  ; logical or
  pop ebx
  pop eax
  cmp eax, 0
  je a_false_{0}
  jmp r_true_{0}
a_false_{0}:
  cmp ebx, 0
  je r_false_{0}
  jmp r_true_{0}
r_true_{0}:
  mov eax, 1
  jmp r_end_{0}
r_false_{0}:
  mov eax, 0
r_end_{0}:
''',
  'not': '''
  ; logical not
  pop eax
  cmp eax, 0
  je r_true_{0}
  jmp r_false_{0}
r_true_{0}:
  mov eax, 1
  jmp r_end_{0}
r_false_{0}:
  mov eax, 0
r_end_{0}:
''',
}

IF_START = '''
  ; if start
  pop eax
  cmp eax, 0
  je else_block_{0}
'''

IF_TRUE_END = '''
'''

ELSE_START = '''
  ; if true end
  jmp if_block_end_{0}
  ; else start
else_block_{0}:
'''

IF_END = '''
  ; if end
if_block_end_{0}:
'''

WHILE_START = '''
  ; while start
while_block_{0}:
'''

WHILE_CONDITION_EVAL = '''
  ; while condition eval
  pop eax
  cmp eax, 0
  je while_block_end_{0}
'''

WHILE_END = '''
  ; while end
  jmp while_block_{0}
while_block_end_{0}:
'''

WHILE_BREAK = '''
  ; while break
  jmp while_block_end_{0}
'''

WHILE_CONTINUE = '''
  ; while continue
  jmp while_block_{0}
'''

FUNCTION_START = '''
  ; function start
  ;jmp function_end_{0}
function_{0}:
  push ebp
  mov ebp, esp
'''

FUNCTION_END = '''
  ; function end
  mov esp, ebp
  pop ebp
  ret
function_end_{0}:
'''

FUNCTION_CALL = '''
  ; function call
  call function_{0}
  add esp, {1}
  ;push eax                     ; push return value
'''

### built-in functions

HEAD = '''global _start

section .text
'''

START = '''
_start:
  push ebp
  mov ebp, esp

  ;call block_0
'''

BLOCK_START = '''
block_{}:
  ; block start
  push ebp
  mov ebp, esp
'''

BLOCK_END = '''
  ; block end
  mov esp, ebp
  pop ebp
  ret
'''

ALLOCATE_LOCAL_VARIABLES = '''
  ; allocate space for local variables
  ;sub esp, {}
'''

EXIT = '''
exit:
  mov ebx, eax
  mov eax, 1
  int 0x80
'''

DEFAULT_EXIT = '''
  ; default exit
  mov eax, 0
  jmp exit
'''

PRINTCHAR = '''
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
'''

PRINT = '''
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
'''
