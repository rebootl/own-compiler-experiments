#!/usr/bin/env python
#
# a toy compiler for a minimal toy language
#

import sys

from assembly import LITERAL, PRIMARIES, UNARIES, BINARIES, \
  HEAD, START, EXIT, DEFAULT_EXIT, PRINTCHAR, PRINT, \
  GET_LOCAL_VARIABLE, COMPARISONS, LOGICALS

OUTFILE = 'out.asm'

INDENT = 2

COMMENT_CHAR = ';'

def collapse_expressions(program):

  """remove newlines while inside parentheses"""

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

  """helper function to split comma-separated arguments"""

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

#LOCAL_VARIABLES = {}

VARIABLE_STACK = []
CURRENT_BLOCK_DEPTH = 0
UNIQUE_COUNTER = 0

def get_unique_count():
  global UNIQUE_COUNTER
  UNIQUE_COUNTER += 1
  return UNIQUE_COUNTER

def check_redeclaration(name):
  #global CURRENT_BLOCK_DEPTH
  #global VARIABLE_STACK

  """check if a variable is defined in the current scope"""
  #print(CURRENT_BLOCK_DEPTH)
  for var in VARIABLE_STACK:
    if var[0] == name and var[1] == CURRENT_BLOCK_DEPTH:
      return True
  return False

def find_variable(name):
  #global VARIABLE_STACK

  """find the stack position of a variable"""

  # we need to find the first occurrence, from the end (top) of the stack
  # but we want to return the index from the start (bottom)
  p = len(VARIABLE_STACK) - 1
  for i, var in enumerate(reversed(VARIABLE_STACK)):
    if var[0] == name:
      return p - i
  return None

def check_arguments(args, num, fn_name=None):
  if len(args) != num:
    if fn_name is None:
      sys.exit("Error: expected " + str(num) + " arguments, got " + str(len(args)))
    else:
      sys.exit("Error: expected " + str(num) + " arguments for " + fn_name + ", got " + str(len(args)))

def parse_expression(expr, asm):
  #global CURRENT_BLOCK_DEPTH
  #global VARIABLE_STACK
  #global UNIQUE_COUNTER
  #UNIQUE_COUNTER += 1
  #print(str(UNIQUE_COUNTER) + " " + expr)

  """parse an expression and return assembly snippet"""

  # trim whitespace
  expr = expr.strip()

  # check for literal
  if expr.isdigit():
    asm += LITERAL.format(expr)
    return asm

  kw = expr.split('(', 1)[0]

  # check for primary
  if kw in PRIMARIES:
    argstr = expr.split('(', 1)[1][:-1]

    if kw == 'println':
      asm += PRIMARIES[kw]
      return asm

    if kw == 'var':
      args = split_args(argstr)

      check_arguments(args, 2, 'var')

      # check that variable name starts with a letter
      if not args[0][0].isalpha():
        sys.exit("Error: variable name must start with a letter")

      if check_redeclaration(args[0]):
        sys.exit("Redeclaration Error: '" + args[0] + "'")

      # this pushes the value onto the stack in asm
      # we leave it there as a local variable
      asm = parse_expression(args[1], asm)

      # store variable name and stack position
      VARIABLE_STACK.append([ args[0], CURRENT_BLOCK_DEPTH ])

      return asm

    if kw == 'set':
      args = split_args(argstr)

      check_arguments(args, 2, 'set')

      stack_pos = find_variable(args[0])
      if stack_pos is None:
        sys.exit("Error setting undeclared variable: '" + args[0] + "'")
      
      # this pushes the value onto the stack in asm
      asm = parse_expression(args[1], asm)

      # this will consume the value on the stack top
      # and update the variable in the correct stack location
      asm += PRIMARIES[kw].format(4 + stack_pos * 4)

      return asm

    # set default exit code
    if kw == 'exit' and argstr == '':
      argstr = '0'

    asm = parse_expression(argstr, asm)

    asm += PRIMARIES[kw]
    return asm

  # check for unary
  if kw in UNARIES:
    arg = expr.split('(', 1)[1][:-1]

    asm = parse_expression(arg, asm)

    asm += UNARIES[kw]
    return asm

  # check for binary
  if kw in BINARIES:
    argstr = expr.split('(', 1)[1][:-1]
    args = split_args(argstr)

    check_arguments(args, 2, kw)

    asm = parse_expression(args[0], asm)
    asm = parse_expression(args[1], asm)
    asm += BINARIES[kw]

    return asm
  
  if kw in COMPARISONS:
    argstr = expr.split('(', 1)[1][:-1]
    args = split_args(argstr)

    check_arguments(args, 2, kw)

    # this pushes the value onto the stack in asm
    asm = parse_expression(args[0], asm)
    asm = parse_expression(args[1], asm)
    asm += COMPARISONS[kw].format(get_unique_count())

    return asm
  
  if kw in LOGICALS:
    argstr = expr.split('(', 1)[1][:-1]

    if kw == 'not':
      asm = parse_expression(argstr, asm)
    else:
      args = split_args(argstr)

      check_arguments(args, 2, kw)

      # this pushes the value onto the stack in asm
      asm = parse_expression(args[0], asm)
      asm = parse_expression(args[1], asm)
    
    asm += LOGICALS[kw].format(get_unique_count())
    return asm

  # check for variable
  stack_pos = find_variable(expr)
  if stack_pos is not None:
    asm += GET_LOCAL_VARIABLE.format(4 + stack_pos * 4)
    return asm

  sys.exit("Unknown keyword: '" + kw + "'")


"""def allocate_local_variables(n_local_vars):

  # create space on the stack for local variables
  #
  # it seems like we don't need to do this, at least not for now,
  # we can just push to the stack directly
  # and it will result in going to the same location as if we allocated,
  # the important part is that the compiler keeps track the locations

  return ALLOCATE_LOCAL_VARIABLES.format(n_local_vars * 4)

BLOCKS = []"""

""" def parse_block_recursive(block):
  
  # parse a block of code recursively
  #
  # we don't need to actually do this
  # for the block / scope we just have to keep track of the local variables
  # and the stack position of each one
  # we don't have to reorder the blocks as i thought first
  #
  # however the code may be useful later for functions

  readahead = False
  indent = 0
  block_lines = []

  n_local_vars = 0

  block_content = ''

  for line in block.splitlines():

    if line == '':
      continue
    if line.lstrip()[0] == COMMENT_CHAR:
      continue

    if readahead:
      line_indent = len(line) - len(line.lstrip())
      if line_indent == indent - INDENT:
        # end of block
        parse_block_recursive('\n'.join(block_lines))
        block_lines = []
        indent -= INDENT
        readahead = False
      
      elif line_indent >= indent:
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
    block_content + \
    BLOCK_END

  BLOCKS.append(block_content) """

def clear_block_stack():
  #global CURRENT_BLOCK_DEPTH
  #global VARIABLE_STACK

  """clear the stack of local variables"""

  for var in reversed(VARIABLE_STACK):
    if var[1] > CURRENT_BLOCK_DEPTH:
      VARIABLE_STACK.pop()

def parse(program):
  global CURRENT_BLOCK_DEPTH
  
  indent = 0
  #block_depth = 0
  #block_count = 0

  main_asm = ''

  for line in program.splitlines():

    if line == '':
      continue
    if line.lstrip()[0] == COMMENT_CHAR:
      continue

    line_indent = len(line) - len(line.lstrip())
    if line_indent < indent:
      # end of block
      closes = (indent - line_indent) / INDENT
      if closes % 1 != 0:
        sys.exit("Indentation error: " + line)

      for i in range(int(closes)):
        indent -= INDENT
        CURRENT_BLOCK_DEPTH -= 1
        clear_block_stack()
    
    elif line_indent > indent:
      # error
      sys.exit("Indentation error: " + line)

    line = line.strip()

    if line[:5] == 'block':
      CURRENT_BLOCK_DEPTH += 1
      indent += INDENT
      #block_count += 1
      continue

    main_asm = parse_expression(line, main_asm)
  
  #main_asm = BLOCK_START.format(0) + \
  #  main_asm + \
  #  BLOCK_END

  return main_asm


def main():

  """main function"""

  # check for program file
  if len(sys.argv) < 2:
    sys.exit("""Usage: compiler.py <program file>
  Output: {}""".format(OUTFILE))

  # open program file
  with open(sys.argv[1], 'r') as f:
    program = f.read()

  # preprocess program
  collapsed_program = collapse_expressions(program)

  # parse program
  main_asm = parse(collapsed_program)

  # combine main assembly code with header, built-in functions and footer
  out = HEAD + EXIT + PRINTCHAR + PRINT + START \
    + main_asm + DEFAULT_EXIT

  # write to output file
  with open(OUTFILE, 'w') as f:
    f.write(out)


# run main function
if __name__ == '__main__':
  main()
