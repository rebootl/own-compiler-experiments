#!/usr/bin/env python
#
# a toy compiler for a minimal toy language v.2
#

import sys

import assembly

OUTFILE = 'out.asm'

INDENT = 2

COMMENT_CHAR = ';'

# def filter_comments(program):

#   """filter out comments from a program"""

#   filtered_program = ''

#   inline_comment = False

#   for c in program:
#     if c == COMMENT_CHAR:
#       inline_comment = True
#       continue
#     elif c == '\n' and inline_comment:
#       inline_comment = False
#       continue
#     elif inline_comment:
#       continue

#     filtered_program += c

#   return filtered_program


def split_expressions(program):

  """split a program into a list of expressions"""

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


#print(split_expressions("a fn (1, 2)\nfn(3, sub(2 , 4)) inc(a)\n"))


def get_kwargstr(s):

  """split a keyword and argument string from an expression"""

  [ kw, argstr ] = s.split('(', 1)

  return [ kw.strip(), argstr.strip()[:-1] ]


def get_split_argstr(argstr):

  """split an argument string into a list of arguments"""

  split_argstr = []
  arg = ''
  depth = 0

  for c in argstr:
    if c == '(':
      depth += 1
    elif c == ')':
      depth -= 1
    elif c == ',' and depth == 0:
      split_argstr.append(arg.strip())
      arg = ''
      continue

    arg += c

  if depth != 0:
    sys.exit("Error: unbalanced parentheses in expression: %s" % argstr)

  if arg != '':
    split_argstr.append(arg.strip())

  return split_argstr

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
    args.append(parse(arg))

  return [ kw, args ]


def eval(expr, asm, depth = 0):

  """evaluate an expression of the form:

  <kw | func> ( <expr> [, <expr>]* )

  """

  if type(expr) == str:

    if expr == '': return asm

    asm += assembly.LITERAL.format(expr)
    return asm

  [ kw, args ] = expr

  for arg in args:
    asm = eval(arg, asm, depth + 1)

  if kw == "exit":
    if len(args) == 0:
      args = [ "0" ]
    asm += assembly.PRIMARIES[kw].format(args[0])

  elif kw == "print":
    asm += assembly.PRIMARIES[kw].format(args[0])

  elif kw == "println":
    if len(args) == 0:
      asm += assembly.PRIMARIES[kw]
    else:
      asm += assembly.PRIMARIES["print"].format(args[0])
      asm += assembly.PRIMARIES[kw]

  elif kw in assembly.BINARIES:
    asm += assembly.BINARIES[kw]

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

  # filter out comments
  #program = filter_comments(program)

  # parse program
  expressions = split_expressions(program)

  parsed_expressions = []
  for expr in expressions:
    parsed_expressions.append(parse(expr))

  # evaluate program
  main_asm = ''
  for expr in parsed_expressions:
    print(expr)
    main_asm = eval(expr, main_asm)

  # combine main assembly code with header, built-in functions and footer
  out = assembly.HEAD + assembly.EXIT + assembly.PRINTCHAR + assembly.PRINT \
    + assembly.START \
    + main_asm + assembly.DEFAULT_EXIT

  # write to output file
  with open(OUTFILE, 'w') as f:
    f.write(out)


# run main function
#if __name__ == '__main__':
#  main()
