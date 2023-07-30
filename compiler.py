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

def stdout(t):
  print(t, file = sys.stderr)

def get_keyword_arg(string):
  # trim whitespace
  s = string.strip()
  l = s.split('(', 1)
  arg = l[1][:-1] # trim last char
  if l[0] not in UNARIES:
    sys.exit("Unknown keyword: " + l[0])
  return l[0], arg

ASM = ""
def parse(code):
  global ASM
  for line in code.splitlines():
    [ kw, arg ] = get_keyword_arg(line)
    if arg.split('(')[0] in UNARIES:
      parse(arg)
    elif arg.isnumeric():
      #print('literal', arg)
      ASM += LITERAL.format(arg)
    #print(kw, arg)
    if kw == 'exit' and arg == '':
      # adding 0 if no argument for default exit
      ASM += LITERAL.format(0)
    ASM += UNARIES[kw]

parse(PROGRAM)

ASM = HEAD + EXIT + PRINTCHAR + PRINT + \
  START + ASM + DEFAULT_EXIT

print(ASM)
