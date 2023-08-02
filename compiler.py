#!/usr/bin/env python
#
# a toy compiler for a minimal toy language
#

import sys

from assembly import LITERAL, PRIMARIES, UNARIES, BINARIES, \
  HEAD, START, EXIT, DEFAULT_EXIT, PRINTCHAR, PRINT, \
  SET_LOCAL_VARIABLE, GET_LOCAL_VARIABLE, DECLARE_LOCAL_VARIABLE

OUTFILE = 'out.asm'

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

  ### helper function to split comma-separated arguments

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

LOCAL_VARIABLES = {}

def parse_expression(expr, repr):

  ### parse an expression and return an intermediate representation

  # trim whitespace
  expr = expr.strip()

  # check for literal
  if expr.isdigit():
    repr += 'LITERAL ' + expr + '\n'
    return repr

  kw = expr.split('(', 1)[0]

  # check for primary
  if kw in PRIMARIES:
    repr += 'PRIMARY ' + kw + '\n'
    return repr

  # check for unary
  if kw in UNARIES:
    arg = expr.split('(', 1)[1][:-1]
    if kw == 'exit' and arg == '':
      repr = parse_expression('0', repr)
    else:
      repr = parse_expression(arg, repr)
    repr += 'UNARY ' + kw + '\n'
    return repr

  # check for binary
  if kw in BINARIES:
    argstr = expr.split('(', 1)[1][:-1]
    args = split_args(argstr)

    if kw == 'var':
      #arg2 = parse_expression(args[1], repr)
      LOCAL_VARIABLES[args[0]] = [ 4 + len(LOCAL_VARIABLES) * 4, args[1] ]
      repr += 'DECLARE ' + args[0] + '\n'

    else:
      repr = parse_expression(args[0], repr)
      repr = parse_expression(args[1], repr)
      repr += 'BINARY ' + kw + '\n'

    return repr

  if kw in LOCAL_VARIABLES:
    repr += 'VARIABLE ' + kw + '\n'
    return repr

  sys.exit("Unknown keyword: '" + kw + "'")


def emit(expr):

  ### emit assembly code from intermediate representation

  [ optype, opval ] = expr.split(' ', 1)
  if optype == 'LITERAL':
    return LITERAL.format(opval)
  if optype == 'PRIMARY':
    return PRIMARIES[opval]
  if optype == 'UNARY':
    return UNARIES[opval]
  if optype == 'BINARY':
    return BINARIES[opval]
  if optype == 'DECLARE':
    return DECLARE_LOCAL_VARIABLE.format(
      LOCAL_VARIABLES[opval][0],
      LOCAL_VARIABLES[opval][1]
    )
  if optype == 'VARIABLE':
    return GET_LOCAL_VARIABLE.format(LOCAL_VARIABLES[opval][0])
  sys.exit("Erroneous intermediate expression: " + expr)


def allocate_local_variables(program):

  ### create space on the stack for local variables

  c = 0
  for line in program.splitlines():
    line = line.strip()
    if line[:3] == 'var':
      c += 1
  return '  sub esp, ' + str(c * 4) + '\n'


def main():

  ### main function

  # check for program file
  if len(sys.argv) < 2:
    sys.exit("""Usage: compiler.py <program file>
  Output: {}""".format(OUTFILE))

  # open program file
  with open(sys.argv[1], 'r') as f:
    program = f.read()

  # preprocess program
  collapsed_program = collapse_expressions(program)

  # parse expressions into intermediate representation
  intermediate_repr = ''
  for line in collapsed_program.splitlines():
    line = line.strip()
    if line == '':
      continue
    if line[0] == '#':
      continue
    intermediate_repr += parse_expression(line, '')

  # emit assembly code from intermediate representation
  main_asm = ''
  for expr in intermediate_repr.splitlines():
    main_asm += emit(expr)

  # allocate space for local variables
  local_vars_alloc = allocate_local_variables(collapsed_program)

  # combine main assembly code with header, built-in functions and footer
  out = HEAD + EXIT + PRINTCHAR + PRINT + \
    START + local_vars_alloc + main_asm + DEFAULT_EXIT

  # write to output file
  with open(OUTFILE, 'w') as f:
    f.write(out)


# run main function
if __name__ == '__main__':
  main()
