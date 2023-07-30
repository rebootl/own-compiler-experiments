#!/usr/bin/env python
#
import sys

from assembly import HEAD, EXIT, PRINTCHAR, PRINT, START, \
  DEFAULT_EXIT, PRINT, LITERAL, UNARIES

if len(sys.argv) < 2:
  sys.exit("Usage: compiler.py <program file>")

# open program file
with open(sys.argv[1], 'r') as f:
  PROGRAM = f.read()

BINARIES = {
  'add': '''
  pop ebx
  pop eax
  add eax, ebx
  push eax
''',
}

def stderr(t):
  print(t, file = sys.stderr)

def get_keyword_arg(string):
  # trim whitespace
  s = string.strip()
  l = s.split('(', 1)
  #stderr('l ' + str(l))
  if len(l) == 1:
    return l[0], None

  arg = l[1][:-1] # trim last char ')'
  return l[0], arg

def get_args(arg):
  args = []
  while arg:
    # Find the first occurrence of '(' and the corresponding closing ')'
    start = arg.find('(')
    if start == -1:
      # No more nested expressions found, add the remaining argument
      args.append(arg.strip())
      arg = None
    else:
      # Extract the nested expression and remove it from the argument string
      end = start + 1
      count = 1
      while count != 0 and end < len(arg):
        if arg[end] == '(':
          count += 1
        elif arg[end] == ')':
          count -= 1
        end += 1
      if count != 0:
        sys.exit("Mismatched parentheses in expression: " + arg)
      args.append(arg[start:end].strip())
      arg = arg[:start] + arg[end:]
  return args

ASM = ""
def parse(code):
  global ASM
  for line in code.splitlines():
    [ kw, arg ] = get_keyword_arg(line)
    if kw in UNARIES:
      if arg:
        parse(arg)
      # adding 0 if no argument for default exit
      if kw == 'exit' and arg == '':
        ASM += LITERAL.format(0)
      #stderr('UNARY ' + kw)
      ASM += UNARIES[kw]
    elif kw in BINARIES:
      args = get_args(arg)
      stderr('BINARY args ' + str(args))
      for arg in args:
        parse(arg)
      #stderr('BINARY ' + kw)
      ASM += BINARIES[kw]
    elif kw.isnumeric():
      #stderr('LITERAL ' + kw)
      ASM += LITERAL.format(kw)
    else:
      sys.exit("Unknown keyword: " + kw)
    #print(kw, arg)

parse(PROGRAM)

ASM = HEAD + EXIT + PRINTCHAR + PRINT + \
  START + ASM + DEFAULT_EXIT

print(ASM)
