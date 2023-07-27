#!/usr/bin/env python
#
import sys

PROGRAM = '''inc(inc(4))
print(5)
exit(10)'''

# x86 assembly chunks

HEAD = '''global _start

section .text
'''

START = '''
_start:
'''

EXIT = '''
exit:
  mov ebx, eax
  mov eax, 1
  int 0x80
'''

PRINT = '''
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
'''

PRINTCHAR = '''
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
'''

KEYWORDS = {
  'exit': '''  jmp exit
''',
  'inc': '''  inc eax
''',
  'dec': '''  dec eax
''',
  'neg': '''  neg eax
''',
  'not': '''  not eax
''',
  'printchar': '''  call printchar
''',
  'print': '''  jmp print
''',
  'LIT': '''  mov eax, {}
'''
}

def stdout(t):
  print(t, file = sys.stderr)

def get_keyword_arg(string):
  # trim whitespace
  s = string.strip()
  l = s.split('(', 1)
  arg = l[1][:-1] # trim last char
  if l[0] not in KEYWORDS:
    sys.exit("Unknown keyword: " + l[0])
  return l[0], arg

ASM = ""
def parse(code):
  global ASM
  for line in code.splitlines():
    [ kw, arg ] = get_keyword_arg(line)
    if arg.split('(')[0] in KEYWORDS:
      parse(arg)
    elif arg.isnumeric():
      #print('literal', arg)
      ASM += KEYWORDS['LIT'].format(arg)
    #print(kw, arg)
    ASM += KEYWORDS[kw]

parse(PROGRAM)

ASM = HEAD + EXIT + PRINTCHAR + PRINT + \
  START + ASM

print(ASM)
