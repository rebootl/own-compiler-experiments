#!/usr/bin/env python
#
#
import sys

PROGRAM = '''
var(a, 5)
var(b, 3)

block:
  set(a, 10)
  set(b, 20)

print(a)
'''

UNARIES = [ 'inc', 'dec', 'print' ]
BINARIES = [ 'add', 'sub', 'var', 'set' ]
BLOCK_STATEMENTS = [ 'block' ]

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

def parse_expression(expr):
  # trim whitespace
  expr = expr.strip()

  # check for literal
  if expr.isdigit():
    print('LITERAL ' + expr)
    return

  # check for unary
  kw = expr.split('(', 1)[0]
  if kw in UNARIES:
    arg = expr.split('(', 1)[1][:-1]
    parse_expression(arg)
    print('UNARY ' + kw)
    return

  # check for binary
  if kw in BINARIES:
    argstr = expr.split('(', 1)[1][:-1]
    #print('BINARY argstr "' + argstr + '"')
    args = split_args(argstr)
    #print('BINARY args ' + str(args))
    parse_expression(args[0])
    parse_expression(args[1])
    print('BINARY ' + kw)
    return

def parse_block(block):
  for line in block.splitlines():
    for kw in BLOCK_STATEMENTS:
      if line.startswith(kw):
        block_lines = []
        indent = 0
        for c in line:
          if c == ' ' or c == '\t':
            indent += 1
          else:
            break
        # -> get next block

        # -> parse block

    parse_expression(line)

def collapse_expressions(program):

  ### remove newlines while inside parentheses

  COLLAPSED_PROGRAM = ''
  count = 0
  for c in program:
    if c == '(':
      count += 1
    elif c == ')':
      count -= 1
    elif c == '\n' and count != 0:
      continue
    COLLAPSED_PROGRAM += c

  return COLLAPSED_PROGRAM

COLLAPSED_PROGRAM = collapse_expressions(PROGRAM)
print(COLLAPSED_PROGRAM)

for line in COLLAPSED_PROGRAM.splitlines():
  parse_expression(line)
