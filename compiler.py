#!/usr/bin/env python
#
# toy compiler
#

import sys

from assembly import LITERAL, PRIMARIES, UNARIES, BINARIES, \
  HEAD, START, EXIT, DEFAULT_EXIT, PRINTCHAR, PRINT

OUTFILE = 'out.asm'

if len(sys.argv) < 2:
  sys.exit("""Usage: compiler.py <program file>
Output: {}""".format(OUTFILE))

# open program file
with open(sys.argv[1], 'r') as f:
  PROGRAM = f.read()

def collapse_expressions(program):

  ### remove newlines while inside parentheses

  collapsed_program = ''
  count = 0
  for c in program:
    if c == '(':
      count += 1
    elif c == ')':
      count -= 1
    elif c == '\n' and count != 0:
      continue
    collapsed_program += c

  return collapsed_program

def split_args(argstr):
  args = []
  arg = ''
  count = 0
  for c in argstr:
    if c == '(':
      count += 1
    elif c == ')':
      count -= 1
    elif c == ',' and count == 0:
      args.append(arg.strip())
      arg = ''
      continue
    arg += c
  if count != 0:
    sys.exit("Mismatched parentheses in expression: " + argstr)
  args.append(arg.strip())
  return args

# intermediate representation
REPR = ""

def parse_expression(expr):
  global REPR
  # trim whitespace
  expr = expr.strip()

  # check for literal
  if expr.isdigit():
    REPR += 'LITERAL ' + expr + '\n'
    return

  kw = expr.split('(', 1)[0]

  # check for primary
  if kw in PRIMARIES:
    REPR += 'PRIMARY ' + kw + '\n'
    return

  # check for unary
  if kw in UNARIES:
    arg = expr.split('(', 1)[1][:-1]
    if kw == 'exit' and arg == '':
      parse_expression('0')
    else:
      parse_expression(arg)
    REPR += 'UNARY ' + kw + '\n'
    return

  # check for binary
  if kw in BINARIES:
    argstr = expr.split('(', 1)[1][:-1]
    args = split_args(argstr)
    parse_expression(args[0])
    parse_expression(args[1])
    REPR += 'BINARY ' + kw + '\n'
    return

  sys.exit("Unknown keyword: '" + kw + "'")


# preprocess program
COLLAPSED_PROGRAM = collapse_expressions(PROGRAM)

for line in COLLAPSED_PROGRAM.splitlines():
  line = line.strip()
  if line == '':
    continue
  if line[0] == '#':
    continue
  parse_expression(line)

# assembly code
ASM = ""

def emit(expr):
  global ASM
  [ optype, opval ] = expr.split(' ', 1)
  if optype == 'LITERAL':
    ASM += LITERAL.format(opval)
  elif optype == 'PRIMARY':
    ASM += PRIMARIES[opval]
  elif optype == 'UNARY':
    ASM += UNARIES[opval]
  elif optype == 'BINARY':
    ASM += BINARIES[opval]
  else:
    sys.exit("Erroneous intermediate expression: " + expr)


for expr in REPR.splitlines():
  emit(expr)

OUT = HEAD + EXIT + PRINTCHAR + PRINT + \
  START + ASM + DEFAULT_EXIT

with open(OUTFILE, 'w') as f:
  f.write(OUT)
