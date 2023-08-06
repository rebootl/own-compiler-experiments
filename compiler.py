#!/usr/bin/env python
#
# a toy compiler for a minimal toy language
#

import sys

from assembly import LITERAL, PRIMARIES, UNARIES, BINARIES, \
  HEAD, START, EXIT, DEFAULT_EXIT, PRINTCHAR, PRINT, \
  ALLOCATE_LOCAL_VARIABLES, SET_LOCAL_VARIABLE, GET_LOCAL_VARIABLE, \
  BLOCK_START, BLOCK_END

OUTFILE = 'out.asm'

INDENT = 2

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

def parse_expression(expr, asm):

  ### parse an expression and return assembly snippet

  # trim whitespace
  expr = expr.strip()

  # check for literal
  if expr.isdigit():
    asm += LITERAL.format(expr)
    return asm

  kw = expr.split('(', 1)[0]

  # check for primary
  if kw in PRIMARIES:
    asm += PRIMARIES[kw]
    return asm

  # check for unary
  if kw in UNARIES:
    arg = expr.split('(', 1)[1][:-1]
    if kw == 'exit' and arg == '':
      asm = parse_expression('0', asm)
    else:
      asm = parse_expression(arg, asm)
    asm += UNARIES[kw]
    return asm

  # check for binary
  if kw in BINARIES:
    argstr = expr.split('(', 1)[1][:-1]
    args = split_args(argstr)

    if kw == 'var':
      if args[0] in LOCAL_VARIABLES:
        sys.exit("Redeclaration Error: '" + args[0] + "'")

      # get value
      asm += parse_expression(args[1], asm)

      stack_pos = 4 + len(LOCAL_VARIABLES) * 4

      # store variable name and stack position
      LOCAL_VARIABLES[args[0]] = [ stack_pos, args[1] ]
      #print(LOCAL_VARIABLES)

      asm += BINARIES[kw].format(stack_pos)

    elif kw == 'set':
      if args[0] not in LOCAL_VARIABLES:
        sys.exit("Error setting undeclared variable: '" + args[0] + "'")

      asm += parse_expression(args[1], asm)

      stack_pos = LOCAL_VARIABLES[args[0]][0]

      LOCAL_VARIABLES[args[0]] = [ stack_pos, args[1] ]

      asm += BINARIES[kw].format(stack_pos)

    else:
      asm = parse_expression(args[0], asm)
      asm = parse_expression(args[1], asm)
      asm += BINARIES[kw]

    return asm

  if kw in LOCAL_VARIABLES:
    asm += GET_LOCAL_VARIABLE.format(LOCAL_VARIABLES[kw][0])
    return asm

  sys.exit("Unknown keyword: '" + kw + "'")


def allocate_local_variables(n_local_vars):

  ### create space on the stack for local variables

  return ALLOCATE_LOCAL_VARIABLES.format(n_local_vars * 4)


def parse_block(block):
  
  readahead = False
  indent = 0
  block_lines = []

  n_local_vars = 0

  block_content = ''

  for line in block.splitlines():

    if line == '':
      continue
    if line[0] == '#':
      continue

    if readahead:
      line_indent = len(line) - len(line.lstrip())
      if line_indent == indent - INDENT:
        # end of block
        block_content += parse_block('\n'.join(block_lines))
        block_lines = []
        readahead = False
        continue
      
      if line_indent >= indent:
        # same or larger indent level
        block_lines.append(line)
        continue
      else:
        # error
        sys.exit("Indentation error: " + line)

    line = line.strip()

    if line[:3] == 'var':
      n_local_vars += 1
    if line[:5] == 'block':
      readahead = True
      indent += INDENT
      continue

    block_content = parse_expression(line, block_content)
  
  block_content = BLOCK_START.format(0) + \
    allocate_local_variables(n_local_vars) + block_content + \
    BLOCK_END

  return block_content


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

  # parse blocks
  block = parse_block(collapsed_program)
  #print(block)

  # combine main assembly code with header, built-in functions and footer
  out = HEAD + EXIT + PRINTCHAR + PRINT \
    + block + START + DEFAULT_EXIT

  # write to output file
  with open(OUTFILE, 'w') as f:
    f.write(out)


# run main function
if __name__ == '__main__':
  main()
