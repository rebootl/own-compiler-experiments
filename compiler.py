#!/usr/bin/env python
#
# a toy compiler for a minimal toy language v.2
#

import sys

import assembly

OUTFILE = 'out.asm'

COMMENT_CHAR = ';'


def split_expressions(program):

  """split a program into a list of expressions,

  filter out comments, and check for balanced parentheses"""

  expressions = []

  expr = ''
  depth = 0

  inline_comment = False

  for c in program:
    if c == COMMENT_CHAR:
      inline_comment = True
      continue
    elif c == '\n' and inline_comment:
      inline_comment = False
      continue
    elif inline_comment:
      continue

    elif c == '(':
      depth += 1
    elif c == ')':
      depth -= 1
      if depth == 0:
        expr += c
        expressions.append(expr.strip())
        expr = ''
        continue

    expr += c

  if depth != 0:
    sys.exit("Error: unbalanced parentheses in program: %s" % program)

  return expressions


def get_kwargstr(s):

  """split a keyword and argument string from an expression"""

  [ kw, argstr ] = s.split('(', 1)

  return [ kw.strip(), argstr.strip()[:-1] ]


def get_split_argstr(argstr):

  """split an argument string into a list of arguments"""

  split_argstr = []
  arg = ''
  depth = 0
  block_depth = 0
  list_depth = 0

  for c in argstr:
    if c == '(':
      depth += 1
    elif c == ')':
      depth -= 1
    elif c == '{':
      block_depth += 1
    elif c == '}':
      block_depth -= 1
    elif c == '[':
      list_depth += 1
    elif c == ']':
      list_depth -= 1
    elif c == ',' and depth == 0 and block_depth == 0 and list_depth == 0:
      split_argstr.append(arg.strip())
      arg = ''
      continue

    arg += c

  if depth != 0:
    sys.exit("Error: unbalanced parentheses in expression: %s" % argstr)

  if block_depth != 0:
    sys.exit("Error: unbalanced curly braces in expression: %s" % argstr)

  if list_depth != 0:
    sys.exit("Error: unbalanced square brackets in expression: %s" % argstr)

  if arg != '':
    split_argstr.append(arg.strip())

  return split_argstr


def check_arguments(args, num, fn_name=None):

  """check that the number of arguments is correct"""

  if len(args) != num:
    if fn_name is None:
      sys.exit("Error: expected " + str(num) + " arguments, got " + str(len(args)))
    else:
      sys.exit("Error: expected " + str(num) + " arguments for " + fn_name + ", got " + str(len(args)))


def parse(expr):

  """parse an expression of the form:

  <kw> ( <expr> [, <expr>]* )

  into a list of keyword and arguments, e.g.:

  [ "fn", [ "1", "2" ] ]
  [ "fn", [ "1", [ "add", [ "2", "3" ] ], [ "sub", [ "4", "5" ] ] ] ]

  """

  if '(' not in expr and ')' not in expr:
    return expr.strip()

  [ kw, argstr ] = get_kwargstr(expr)

  split_argstr = get_split_argstr(argstr)

  args = []
  for arg in split_argstr:
    if arg.lstrip().startswith('{'):
      args.append(arg)
    else:
      args.append(parse(arg))

  return [ kw, args ]


STACK_FRAMES = [ {
      'params': [],
      'vars': [ [] ],   # blocks
} ]

UNIQUE_COUNTER = 0

LOOP_IDS = []

FUNCTIONS = {}

LITERALS = []

def get_unique_count():
  global UNIQUE_COUNTER
  UNIQUE_COUNTER += 1
  return UNIQUE_COUNTER

def find_variable(name, stack_frame):

  """find the stack position of a variable"""

  # we need to find the first occurrence, from the end (top) of the stack
  # but we want to return the index from the start (bottom)
  r = None
  c = 0
  for block in stack_frame:
    for var in block:
      if var == name:
        r = c
      c += 1
  return r

def find_parameter(name, stack_frame):

  """find the stack position of a parameter"""

  # we need to find the first occurrence, from the end (top) of the stack
  for i, param in enumerate(reversed(stack_frame)):
    if param[0] == name:
      return i
  return None

def eval_block(block, asm, depth):

  STACK_FRAMES[-1]['vars'].append([])

  block_exprs = split_expressions(block.strip()[1:-1])
  for expr in block_exprs:
    asm = eval(parse(expr), asm, depth + 1)

  for var in STACK_FRAMES[-1]['vars'][-1]:
    asm += assembly.POP_LOCAL_VARIABLE

  STACK_FRAMES[-1]['vars'].pop()

  return asm

def get_list_args(list_str):

  r = [ x.strip() for x in list_str.strip()[1:-1].split(',') ]

  if r == ['']: return []
  return r


def eval(expr, asm, depth = 0):

  """evaluate an expression of the form:

  <kw | func> ( <expr> [, <expr>]* )

  """

  #print(expr)

  if type(expr) == str:

    if expr == '': return asm

    # check for variable
    stack_pos = find_variable(expr, STACK_FRAMES[-1]['vars'])

    if stack_pos is not None:
      asm += assembly.GET_LOCAL_VARIABLE.format(4 + stack_pos * 4)
      return asm

    # check for parameter
    stack_pos = find_parameter(expr, STACK_FRAMES[-1]['params'])

    if stack_pos is not None:
      asm += assembly.GET_PARAMETER.format(8 + stack_pos * 4)
      return asm

    if expr.isdigit():
      asm += assembly.LITERAL.format(expr)
      return asm

    # negative numbers
    if expr.startswith('-') and expr[1:].isdigit():
      asm += assembly.LITERAL.format(expr)
      return asm

  [ kw, args ] = expr

  if kw == "var":
    check_arguments(args, 2, 'var')

    # check that variable name starts with a letter
    if not args[0][0].isalpha():
      sys.exit("Error: variable name must start with a letter")

    if args[0] in STACK_FRAMES[-1]['vars'][-1]:
      sys.exit("Redeclaration Error: '" + args[0] + "'")

    # this pushes the value onto the stack in asm
    # we leave it there as a local variable
    asm = eval(args[1], asm, depth + 1)
    asm += assembly.PUSH_RESULT

    # store variable in comp.
    STACK_FRAMES[-1]['vars'][-1].append(args[0])

    return asm

  if kw == 'set':
    check_arguments(args, 2, 'set')

    stack_pos = find_variable(args[0], STACK_FRAMES[-1]['vars'])
    if stack_pos is None:
      sys.exit("Error setting undeclared variable: '" + args[0] + "'")

    # this pushes the value onto the stack in asm
    asm = eval(args[1], asm, depth + 1)
    asm += assembly.PUSH_RESULT

    # this will consume the value on the stack top
    # and update the variable in the correct stack location
    asm += assembly.PRIMARIES[kw].format(4 + stack_pos * 4)

    return asm

  if kw == 'block':
    asm = eval_block(args[0], asm, depth)

    return asm

  if kw == 'if':
    # get id for block
    id = get_unique_count()

    # eval condition
    asm = eval(args[0], asm, depth + 1)
    asm += assembly.PUSH_RESULT

    asm += assembly.IF_START.format(id)

    asm = eval_block(args[1], asm, depth)

    if len(args) == 3:
      asm += assembly.ELSE_START.format(id)

      asm = eval_block(args[2], asm, depth)

    else:
      asm += assembly.ELSE_START.format(id)

    asm += assembly.IF_END.format(id)

    return asm

  if kw == 'while':
    # get id for block
    id = get_unique_count()

    asm += assembly.WHILE_START.format(id)

    # eval condition
    asm = eval(args[0], asm, depth + 1)
    asm += assembly.PUSH_RESULT

    # emit condition evaluation
    asm += assembly.WHILE_CONDITION_EVAL.format(id)

    LOOP_IDS.append(id)
    asm = eval_block(args[1], asm, depth)
    LOOP_IDS.pop()

    asm += assembly.WHILE_END.format(id)

    return asm

  if kw == 'function':
    check_arguments(args, 3, 'function')

    # check that function name starts with a letter
    if not args[0][0].isalpha():
      sys.exit("Error: function name must start with a letter")

    params = get_list_args(args[1])

    FUNCTIONS[args[0]] = 1

    # push a new frame onto the stack_frames
    STACK_FRAMES.append({
      'params': [],
      'vars': [],
    })

    # check that parameter names start with a letter
    for param in params:
      if not param[0].isalpha():
        sys.exit("Error: parameter name must start with a letter")

      STACK_FRAMES[-1]['params'].append(param)

    fn_asm = ""
    fn_asm += assembly.FUNCTION_START.format(args[0])

    fn_asm = eval_block(args[2], fn_asm, 0)

    fn_asm += assembly.FUNCTION_END.format(args[0])

    FUNCTIONS[args[0]] = fn_asm

    STACK_FRAMES.pop()

    return asm

  if kw == 'prints':
    check_arguments(args, 1, 'prints')
    arg = args[0]
    if arg.startswith("'") and arg.endswith("'"):
      # push string onto stack
      #for char in reversed(arg[1:-1]):
      #  asm += assembly.PUSH_CHAR.format(ord(char))
      #asm += assembly.PRIMARIES[kw]
      #asm += assembly.CLEAR_STACK.format(len(arg) * 4)

      # emit literal to .data section
      str_id = 'string_' + str(get_unique_count())
      LITERALS.append(assembly.DATA_STRING.format(
        str_id,
        arg[1:-1]
      ))
      asm += assembly.PUSH_STR_REF.format(str_id)
      asm += assembly.PRIMARIES[kw]
      # -> clear stack
    else:
      sys.exit("Error: prints only accepts strings")

    return asm

  for arg in args:
    asm = eval(arg, asm, depth + 1)
    asm += assembly.PUSH_RESULT

  if kw == "exit":
    if len(args) == 0:
      args = [ "0" ]
    asm += assembly.PRIMARIES[kw].format(args[0])

  elif kw == "print":
    check_arguments(args, 1, 'print')
    asm += assembly.PRIMARIES[kw].format(args[0])

  elif kw == "println":
    if len(args) == 0:
      asm += assembly.PRIMARIES[kw]
    else:
      asm += assembly.PRIMARIES["print"].format(args[0])
      asm += assembly.PRIMARIES[kw]

  elif kw == "return":
    asm += assembly.PRIMARIES[kw]

  elif kw == 'inc' or kw == 'dec':
    check_arguments(args, 1, 'inc/dec')

    stack_pos = find_variable(args[0], STACK_FRAMES[-1]['vars'])
    if stack_pos is None:
      sys.exit("Error in inc/dec: variable '" + args[0] + "' not found")

    asm += assembly.PRIMARIES[kw].format(4 + stack_pos * 4)

  elif kw in assembly.UNARIES:
    check_arguments(args, 1, kw)

    asm += assembly.UNARIES[kw]

  elif kw in assembly.BINARIES:
    check_arguments(args, 2, kw)

    asm += assembly.BINARIES[kw]

  elif kw in assembly.COMPARISONS:
    check_arguments(args, 2, kw)

    # this pushes the value onto the stack in asm
    asm += assembly.COMPARISONS[kw].format(get_unique_count())

  elif kw in assembly.LOGICALS:
    if kw == 'not':
      check_arguments(args, 1, kw)
    else:
      check_arguments(args, 2, kw)

    asm += assembly.LOGICALS[kw].format(get_unique_count())

  elif kw == 'check_overflow':
    id = get_unique_count()
    asm += assembly.CHECK_OVERFLOW.format(id)

  elif kw == 'break':
    asm += assembly.WHILE_BREAK.format(LOOP_IDS[-1])

  elif kw == 'continue':
    asm += assembly.WHILE_CONTINUE.format(LOOP_IDS[-1])

  elif kw in FUNCTIONS:
    asm += assembly.FUNCTION_CALL.format(kw, len(args) * 4)

  else:
    sys.exit("Error: unknown keyword '" + kw + "'")

  return asm


def main():

  """main function"""

  # check for program file
  if len(sys.argv) < 2:
    sys.exit("""Usage: compiler.py <program file>
  Output: {}""".format(OUTFILE))

  # open program file
  with open(sys.argv[1], 'r') as f:
    program = f.read()

  # parse program
  expressions = split_expressions(program)

  parsed_expressions = []
  for expr in expressions:
    parsed_expressions.append(parse(expr))

  # evaluate program
  main_asm = ''
  for expr in parsed_expressions:
    #print(expr)
    main_asm = eval(expr, main_asm)

  fns_asm = ""
  for fn in FUNCTIONS:
    fns_asm += FUNCTIONS[fn]

  # combine main assembly code with header, built-in functions and footer
  out = assembly.DATA + ''.join(LITERALS) + '\n' \
    + assembly.HEAD + assembly.EXIT + assembly.PRINTCHAR + assembly.PRINT \
    + fns_asm \
    + assembly.START \
    + main_asm + assembly.DEFAULT_EXIT

  # write to output file
  with open(OUTFILE, 'w') as f:
    f.write(out)


# run main function
if __name__ == '__main__':
  main()
