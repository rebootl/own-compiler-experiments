#!/usr/bin/env python
#
import sys

from assembly import HEAD, EXIT, PRINTCHAR, PRINT, START, \
  DEFAULT_EXIT, PRINT

if len(sys.argv) < 2:
  sys.exit("Usage: compiler.py <program file>")

# open program file
with open(sys.argv[1], 'r') as f:
  PROGRAM = f.read()

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
  'printchar': '''
  push eax
  call printchar
''',
  'println': '''
  push 10
  call printchar
  add esp, 8
''',
  'print': '''
  push edx
  push ecx
  push eax
  call print_int
  pop eax
  pop ecx
  pop edx
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
  START + ASM + DEFAULT_EXIT

print(ASM)
