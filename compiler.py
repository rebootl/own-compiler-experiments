#!/usr/bin/env python
#
# a toy compiler for a minimal toy language
#

import sys

from assembly import LITERAL, PRIMARIES, UNARIES, BINARIES, \
  HEAD, START, EXIT, DEFAULT_EXIT, PRINTCHAR, PRINT, \
  GET_LOCAL_VARIABLE, COMPARISONS, LOGICALS, \
  IF_START, IF_TRUE_END, ELSE_START, IF_END, \
  WHILE_START, WHILE_CONDITION_EVAL, WHILE_END, \
  POP_LOCAL_VARIABLE, CHECK_OVERFLOW, WHILE_BREAK, WHILE_CONTINUE, \
  FUNCTION_START, FUNCTION_END, FUNCTION_CALL

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

  """helper function to split comma-separated arguments

  e.g.: '1, 2, 3' -> [ '1', '2', '3' ]
        '1, add(2, 3)' -> [ '1', 'add(2, 3)' ]

  """

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


UNIQUE_COUNTER = 0

def get_unique_count():
  global UNIQUE_COUNTER
  UNIQUE_COUNTER += 1
  return UNIQUE_COUNTER


CURRENT_INDENT = 0

def increment_indent():
  global CURRENT_INDENT
  CURRENT_INDENT += INDENT

def decrement_indent():
  global CURRENT_INDENT
  CURRENT_INDENT -= INDENT


def get_current_block_depth():
  return CURRENT_INDENT / INDENT


VARIABLE_STACK = []

FUNCTIONS = {}

STACK_FRAMES = [ [] ]

def check_redeclaration(name, stack_frame):

  """check if a variable is defined in the current scope"""

  for var in stack_frame:
    if var[0] == name and var[1] == get_current_block_depth():
      return True
  return False

def find_variable(name, stack_frame):

  """find the stack position of a variable"""

  # we need to find the first occurrence, from the end (top) of the stack
  # but we want to return the index from the start (bottom)
  p = len(stack_frame) - 1
  for i, var in enumerate(reversed(stack_frame)):
    if var[0] == name:
      return p - i
  return None

def check_arguments(args, num, fn_name=None):

  """check that the number of arguments is correct"""

  if len(args) != num:
    if fn_name is None:
      sys.exit("Error: expected " + str(num) + " arguments, got " + str(len(args)))
    else:
      sys.exit("Error: expected " + str(num) + " arguments for " + fn_name + ", got " + str(len(args)))

def get_kwargstr(expr):

  """helper function to split keyword and argument string

  -> make this split arguments automatically

  e.g.: 'print(1)' -> [ 'print', '1' ]
        'var(x, 1)' -> [ 'var', 'x, 1' ]
        'add(1, add(2, 3))' -> [ 'add', '1, add(2, 3)' ]
  """

  s = expr.split('(', 1)
  if len(s) == 1:
    return [ s[0], '' ]
  
  if s[1].strip().startswith(')'):
    return [ s[0], '' ]

  return [ s[0], s[1][:-1] ]

def parse_expression(expr, asm, level = 0):

  """recursively parse an expression and return assembly snippet
  
  level is the nesting level of the expression, used to check for
  nested primaries
  
  """

  # trim whitespace
  expr = expr.strip()

  # check for literal
  if expr.isdigit():
    asm += LITERAL.format(expr)
    return asm

  [ kw, argstr ] = get_kwargstr(expr)

  # check for primary
  if kw in PRIMARIES:

    if level > 0:
      sys.exit("Error: primary '" + kw + "' cannot be nested")

    if kw == 'println':
      asm += PRIMARIES[kw]
      return asm

    if kw == 'inc' or kw == 'dec':
      check_arguments(argstr, 1, 'inc/dec')

      stack_pos = find_variable(argstr, STACK_FRAMES[-1])
      if stack_pos is None:
        sys.exit("Error in inc/dec: variable '" + argstr + "' not found")
      
      asm += PRIMARIES[kw].format(4 + stack_pos * 4)
      return asm

    if kw == 'var':
      args = split_args(argstr)

      check_arguments(args, 2, 'var')

      # check that variable name starts with a letter
      if not args[0][0].isalpha():
        sys.exit("Error: variable name must start with a letter")

      if check_redeclaration(args[0], STACK_FRAMES[-1]):
        sys.exit("Redeclaration Error: '" + args[0] + "'")

      # this pushes the value onto the stack in asm
      # we leave it there as a local variable
      asm = parse_expression(args[1], asm, level + 1)

      # store variable name and stack position
      STACK_FRAMES[-1].append([ args[0], get_current_block_depth() ])

      return asm

    if kw == 'set':
      args = split_args(argstr)

      check_arguments(args, 2, 'set')

      stack_pos = find_variable(args[0], STACK_FRAMES[-1])
      if stack_pos is None:
        sys.exit("Error setting undeclared variable: '" + args[0] + "'")
      
      # this pushes the value onto the stack in asm
      asm = parse_expression(args[1], asm, level + 1)

      # this will consume the value on the stack top
      # and update the variable in the correct stack location
      asm += PRIMARIES[kw].format(4 + stack_pos * 4)

      return asm

    # set default exit code
    if kw == 'exit' and argstr == '':
      argstr = '0'

    asm = parse_expression(argstr, asm, level + 1)

    asm += PRIMARIES[kw]
    return asm

  # check for unary
  if kw in UNARIES:

    asm = parse_expression(argstr, asm, level + 1)

    asm += UNARIES[kw]
    return asm

  # check for binary
  if kw in BINARIES:

    args = split_args(argstr)

    check_arguments(args, 2, kw)

    asm = parse_expression(args[0], asm, level + 1)
    asm = parse_expression(args[1], asm, level + 1)
    asm += BINARIES[kw]

    return asm
  
  if kw in COMPARISONS:

    args = split_args(argstr)

    check_arguments(args, 2, kw)

    # this pushes the value onto the stack in asm
    asm = parse_expression(args[0], asm, level + 1)
    asm = parse_expression(args[1], asm, level + 1)
    asm += COMPARISONS[kw].format(get_unique_count())

    return asm
  
  if kw in LOGICALS:

    if kw == 'not':
      asm = parse_expression(argstr, asm, level + 1)
    else:
      args = split_args(argstr)

      check_arguments(args, 2, kw)

      # this pushes the value onto the stack in asm
      asm = parse_expression(args[0], asm, level + 1)
      asm = parse_expression(args[1], asm, level + 1)
    
    asm += LOGICALS[kw].format(get_unique_count())
    return asm

  if kw == 'check_overflow':
    id = get_unique_count()
    asm += CHECK_OVERFLOW.format(id)
    return asm

  # check for variable
  stack_pos = find_variable(expr, STACK_FRAMES[-1])
  if stack_pos is not None:
    asm += GET_LOCAL_VARIABLE.format(4 + stack_pos * 4)
    return asm
  
  # check for function
  print(FUNCTIONS)
  if kw in FUNCTIONS:
    # args = split_args(argstr)

    # check_arguments(args, FUNCTIONS[kw], kw)

    # for arg in args:
    #   asm = parse_expression(arg, asm, level + 1)
    
    asm += FUNCTION_CALL.format(kw)
    return asm

  sys.exit("Unknown keyword: '" + kw + "'")


def clear_block_stack_variables(stack_frame):

  """clear the stack of local variables"""

  c = 0
  for var in reversed(stack_frame):
    if var[1] > get_current_block_depth():
      stack_frame.pop()
      c += 1
  
  return c

def parse(program):

  main_asm = ''

  block_stack = []

  for line in program.splitlines():

    if line == '':
      continue
    if line.lstrip() == '':
      continue
    if line.lstrip()[0] == COMMENT_CHAR:
      continue

    line_indent = len(line) - len(line.lstrip())
    if line_indent < CURRENT_INDENT:
      # end of block
      closes = (CURRENT_INDENT - line_indent) / INDENT
      if closes % 1 != 0:
        sys.exit("Indentation error (less): " + line)

      for i in range(int(closes)):
        decrement_indent()

        # -> these pop local variables off the stack
        #    for functions this is not necessary
        n = clear_block_stack_variables(STACK_FRAMES[-1])
        
        for j in range(n):
          main_asm += POP_LOCAL_VARIABLE

        block = block_stack.pop()

        if block[0] == 'IF_BLOCK':
          # end of if block
          if CURRENT_INDENT * ' ' + 'else:' == line:
            increment_indent()
            
            main_asm += ELSE_START.format(block[1])
            block_stack.append([ 'ELSE_BLOCK', block[1] ])
          else:
            main_asm += ELSE_START.format(block[1])
            main_asm += IF_END.format(block[1])
        
        elif block[0] == 'ELSE_BLOCK':
          # end of else block
          main_asm += IF_END.format(block[1])
        
        elif block[0] == 'WHILE_BLOCK':
          # end of while block
          main_asm += WHILE_END.format(block[1])
        
        elif block[0] == 'FUNCTION_BLOCK':
          # end of function block
          main_asm += FUNCTION_END.format(block[1])

          STACK_FRAMES.pop()
    
    elif line_indent > CURRENT_INDENT:
      # error
      sys.exit("Indentation error: " + line)

    line = line.strip()

    if line.startswith('block'):
      increment_indent()
      block_stack.append([ 'BLOCK', None ])
      continue
    
    if line.startswith('if'):
      increment_indent()

      # get id for block
      id = get_unique_count()

      block_stack.append([ 'IF_BLOCK', id ])

      # parse condition
      condition = line.split('(', 1)[1][:-2]
      main_asm = parse_expression(condition, main_asm)

      # emit if block start
      main_asm += IF_START.format(id)

      continue
    
    if line.startswith('else'):
      continue
    
    if line.startswith('while'):
      increment_indent()

      # get id for block
      id = get_unique_count()

      block_stack.append([ 'WHILE_BLOCK', id ])

      # parse condition
      condition = line.split('(', 1)[1][:-2]
      condition_asm = parse_expression(condition, '')

      # emit while block start
      main_asm += WHILE_START.format(id)

      # emit condition
      main_asm += condition_asm

      # emit condition evaluation
      main_asm += WHILE_CONDITION_EVAL.format(id)

      continue
    
    if line.startswith('break') or line.startswith('continue'):
      while_found = False
      for block in reversed(block_stack):
        if block[0] == 'WHILE_BLOCK':
          if line.startswith('continue'):
            main_asm += WHILE_CONTINUE.format(block[1])
          else:
            main_asm += WHILE_BREAK.format(block[1])
          while_found = True
          break
  
      if not while_found:
        sys.exit("Error: break outside of while loop")

      continue
    
    if line.startswith('function'):
      increment_indent()
      
      # split on white space
      kwargstr = line.split(None, 1)[1]
      [ name, argstr ] = get_kwargstr(kwargstr)
      #print("Function: " + str(name) + " " + str(argstr))

      # -> check name redeclaration

      # get id for block
      #id = get_unique_count()

      block_stack.append([ 'FUNCTION_BLOCK', name ])

      FUNCTIONS[name] = 1

      # push a new frame onto the stack_frames
      STACK_FRAMES.append([])

      # -> parse arguments

      # emit function start
      main_asm += FUNCTION_START.format(name)

      continue
    
    main_asm = parse_expression(line, main_asm)
    #print("Line: " + line)
    #print(STACK_FRAMES)

  # close remaining open blocks at EOF

  while len(block_stack) > 0:
    block = block_stack.pop()
    if block[0] == 'IF_BLOCK' or block[0] == 'ELSE_BLOCK':
      main_asm += IF_END.format(block[1])
    elif block[0] == 'WHILE_BLOCK':
      decrement_indent()
      n = clear_block_stack_variables(STACK_FRAMES[-1])

      for j in range(n):
        main_asm += POP_LOCAL_VARIABLE
      main_asm += WHILE_END.format(block[1])

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
