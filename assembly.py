# assembly chunks
#
# 32-bit x86 nasm assembly
#

CLEAR_STACK = '''
  ; add esp
  add esp, {0}
'''

DATA_STRING = '''
  {0} db `{1}`, 0
'''

PUSH_STR_REF = '''
  ; push string reference
  push {0}
'''

PUSH_RESULT = '''
  ; push result
  push eax
'''

PUSH_CHAR = '''
  ; push char
  push {}
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

EXT_FREE_STR = '''
  ; free string
  mov ebx, eax
  call free_str
  add esp, 4      ; clear stack
  mov eax, ebx
'''

CALL_EXTENSION = '''
  ; call extension
  call {0}
'''

# CALL_EXTENSION = {
#   'print_i': '''
#   ; call print extension
#   call print_i
#   ;add esp, 4      ; clear stack
# ''',
#   'print': '''
#   ; call print extension
#   call print
#   ;add esp, 4      ; clear stack
# ''',
# #  'print_free': '''
# #  ; call print extension
# #  call print
# #  call free_str
# #  add esp, 4      ; clear stack
# #''',
#   'println': '''
#   ; call println extension
#   call println
# ''',
#   'Int2Str': '''
#   ; call int_to_str extension
#   call int_to_str
#   ;add esp, 4      ; clear stack
# ''',
#   'String': '''
#   ; call string extension
#   call allocate_str
#   ;add esp, 4      ; clear stack
# ''',
#   'Concat': '''
#   ; call concat extension
#   call concat
#   ;add esp, 8      ; clear stack
# ''',
#   'Substr': '''
#   ; call substr extension
#   call substr
# ''',
#   'Reverse': '''
#   ; call reverse extension
#   call reverse
# ''',
#   'Upper': '''
#   ; call upper extension
#   call uppercase
# ''',
#   'Lower': '''
#   ; call lower extension
#   call lowercase
# ''',
#   'len': '''
#   ; call len extension
#   call len
# ''',
# }

PRIMARIES = {
  'exit': '''
  ; jump to exit
  pop eax
  jmp exit
''',
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
  mov esp, ebp
  pop ebp
  ret
''',
}

UNARIES = {
  'neg': '''
  ; negate stack top
  pop eax
  not    eax            ; negate eax
  inc    eax            ; add 1
''',
  'abs': '''
  ; absolute value stack top
  pop eax
  cdq                   ; convert to double word
  xor eax, edx          ; xor eax with edx
  sub eax, edx          ; subtract edx from eax
''',
}

BINARIES = {
  'add': '''
  ; add stack top
  pop eax
  pop ebx
  add eax, ebx
  ;push eax
''',
  'sub': '''
  ; subtract stack top
  pop eax
  pop ebx
  sub eax, ebx
  ;push eax
''',
  'mul': '''
  ; multiply stack top
  pop eax
  pop ebx
  imul eax, ebx
  ;push eax
''',
  'div': '''
  ; divide stack top
  pop eax
  pop ebx
  cdq
  idiv ebx
  ;push eax
''',
  'mod': '''
  ; modulus stack top
  pop eax
  pop ebx
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
  pop eax
  pop ebx
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
  pop eax
  pop ebx
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
  pop eax
  pop ebx
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
  ;add esp, {1}
'''

### built-in functions

HEAD = '''extern print_i, println, print, allocate_str, String, Int2str, Concat
extern Substr, Revstr, Upper, Lower, len, free_str
global {}
'''

DATA = '''
section .data
'''

TEXT = '''
section .text
'''

START = '''
{}:
  push ebp
  mov ebp, esp

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
