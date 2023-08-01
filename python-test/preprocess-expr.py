#!/usr/bin/env python
#
#
import sys

PROGRAM = '''5
inc(1)
add(
  inc(1),
  add(2, dec(3))
)

add(
  sub(5, 2),
  sub(3, 1)
)
'''

UNARIES = [ 'inc', 'dec' ]
BINARIES = [ 'add', 'sub' ]

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
