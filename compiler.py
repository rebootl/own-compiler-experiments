#!/usr/bin/env python
#
# a toy compiler for a minimal toy language v.2
#

import sys

import assembly


### config

OUTFILE = 'out.asm'

COMMENT_CHAR = ';'

# for ld linker use '_start'
START_LABEL = 'main'


### global variables, state

# a list of stack frames used during compilation to keep track of parameters
# and local variables
# e.g.: [ {
#   'name': <function name>,
#   'params': [ [ <param name>, <param type> ], ... ],
#   'vars': [ [ [ <var name>, <var type> ], ... ], ... ],
#   'return_type': <return type>
# } ]
# during compilation, every function will push a new stack frame, and pop it
# at the end of the function
# to keep track of functions after their evaluation, we will use the FUNCTIONS
# dictionary below
STACK_FRAMES = [ {
    'name': 'main',
    'params': [],
    'vars': [ [] ],   # blocks
    'return_type': 'UNDEF'
} ]

# a simple unique counter
UNIQUE_COUNTER = 0

# accessor for the unique counter
def get_unique_count():
  global UNIQUE_COUNTER
  UNIQUE_COUNTER += 1
  return UNIQUE_COUNTER

# a list of loop ids, we need these for break/continue
# form: [ [ <loop id>, <position of the loop in the block stack> ], ... ]
# the position in the block stack is used to free the variables,
# when using break or continue
LOOP_IDS = []

# functions of the form:
#   'fn': {
#     'param_types': [ 'INT', 'INT', ... ]
#     'return_type': 'INT',
#     'asm': 'asm code'
#    }
#
# this has to be kept separately from the stack frames, because
# the stack frame is adapting dynamically
FUNCTIONS = {}

# assembly code of the literals that will go to the data section
LITERALS = []


def free_string(asm, stack_pos):
  asm += assembly.GET_LOCAL_VARIABLE.format(4 + stack_pos * 4)
  asm += assembly.PUSH_RESULT
  asm += assembly.EXT_FREE_STR


def free_array(asm, stack_pos):
  asm += assembly.GET_LOCAL_VARIABLE.format(4 + stack_pos * 4)
  asm += assembly.PUSH_RESULT
  asm += assembly.EXT_FREE_ARRAY


# type definitions
TYPES = {
  'UNDEF': {
    'enum': None,
    'has_memory': False,
  },
  'STRING_LIT': {
    'enum': None,
    'has_memory': False,
  },
  'INT': {
    'enum': 0,
    'has_memory': False,
  },
  'STRING': {
    'enum': 1,
    'has_memory': True,
    'free_function': free_string,
  },
  'ARRAY': {
    'enum': 2,
    'has_memory': True,
    'free_function': free_array,
  },
}



# extensions, calling c code
EXTENSIONS = {
  'print': {
    'arg_types': [ [ 'STRING_LIT', 'STRING' ] ],
  },
  'print_i': {
    'arg_types': [ 'INT' ],
  },
  'Int2str': {
    'arg_types': [ 'INT' ],
    'return_type': 'STRING',
  },
  'String': {
    'arg_types': [ [ 'STRING_LIT', 'STRING' ] ],
    'return_type': 'STRING',
  },
  'Concat': {
    'arg_types': [ [ 'STRING_LIT', 'STRING' ], [ 'STRING_LIT', 'STRING' ] ],
    'return_type': 'STRING',
  },
  'Substr': {
    'arg_types': [ [ 'STRING_LIT', 'STRING' ], 'INT', 'INT' ],
    'return_type': 'STRING',
  },
  'Revstr': {
    'arg_types': [ [ 'STRING_LIT', 'STRING' ] ],
    'return_type': 'STRING',
  },
  'Upper': {
    'arg_types': [ [ 'STRING_LIT', 'STRING' ], 'INT', 'INT' ],
    'return_type': 'STRING',
  },
  'Lower': {
    'arg_types': [ [ 'STRING_LIT', 'STRING' ], 'INT', 'INT' ],
    'return_type': 'STRING',
  },
  'len': {
    'arg_types': [ [ 'STRING_LIT', 'STRING' ] ],
    'return_type': 'INT',
  },
  'get': {
    'arg_types': [ 'INT', [ 'ARRAY', 'INT' ] ],
    'return_type': 'INT',
  },
  'addr2str': {
    'arg_types': [ 'INT' ],
    'return_type': 'STRING',
  },
}


### helper

def flatten(l):

  """flatten a list of lists"""

  return [item for sublist in l for item in sublist]


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
  #print('kw: ' + kw)
  #print('argstr: ' + argstr)

  return [ kw.strip(), argstr.strip()[:-1] ]


def get_split_argstr(argstr):

  """split an argument string into a list of arguments"""

  split_argstr = []
  arg = ''
  depth = 0
  block_depth = 0
  list_depth = 0
  string_lit = False

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
    elif c == "'":
      string_lit = not string_lit
    elif string_lit and c == '\n':
      c = '\\n'
    elif c == ',' and depth == 0 and block_depth == 0 and list_depth == 0 and not string_lit:
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


def check_arg_types(kw, arg_types, expected_types):

  """this just compares two lists of types, and exits with an error if they don't match,

  e.g. check_arg_types('add', ['INT', 'INT'], ['INT', 'INT'])

  kw is used for the error message only

  """

  if len(arg_types) != len(expected_types):
    sys.exit("Error: expected %d arguments for %s, got %d" % (len(expected_types), kw, len(arg_types)))

  for i, _type in enumerate(reversed(arg_types)):
    if type(expected_types[i]) == list:
      if _type not in expected_types[i]:
        sys.exit("Error: expected type %s for argument %d of %s, got %s" % (expected_types[i], i + 1, kw, _type))
    elif _type != expected_types[i]:
      sys.exit("Error: expected type %s for argument %d of %s, got %s" % (expected_types[i], i + 1, kw, _type))


def find_variable(name, stack_frame):

  """find the stack position of a variable, also return its type"""

  # we need to find the first occurrence, from the end (top) of the stack
  # but we want to return the index from the start (bottom)

  # [ <stack_position>, <type> ]
  r = [ None, None ]
  for i, var in enumerate(flatten(stack_frame)):
    if var[0] == name:
      r = [ i, var[1] ]
  return r


def find_parameter(name, stack_frame):

  """find the stack position of a parameter, also return its type"""

  # we need to find the first occurrence, from the end (top) of the stack
  for i, param in enumerate(stack_frame):
    if param[0] == name:
      return [ i, param[1] ]
  return [ None, None ]


def check_redeclaration_parameter(args):
  for param in STACK_FRAMES[-1]['params']:
    if param[0] == args[0]:
      sys.exit("Redeclaration Error(parameter): '" + args[0] + "'")
    # disallow parameters move into local variable for now
    if param[0] == args[1]:
      sys.exit("Error: cannot move parameter: '" + args[1] + "'")


def move_ownership(var_name, type):
  # if the 2nd argument is a variable and it has memory allocated,
  # we want to set it's type to 'UNDEF', in order to avoid freeing
  # it twice
  # this is equivalent to a move of ownership
  #
  # alternatively we could allocate a string on the heap and copy
  # the value of the variable
  [ arg1_stack_pos, arg1_type ] = find_variable(var_name, STACK_FRAMES[-1]['vars'])

  if TYPES[type]['has_memory'] and arg1_stack_pos is not None:
    for var in reversed(flatten(STACK_FRAMES[-1]['vars'])):
      if var[0] == var_name:
        var[1] = 'UNDEF'
        break

    # TYPES[arg1_type]['free_function'](asm, arg1_stack_pos)


def free_at_loop_break():
  # -> this code is kind of terrible... we keep track of the position
  #    of the loop block in the stack of blocks in the LOOP_IDS list,
  #    when breaking we need to free all the variables in the block
  #    and subsequent blocks
  asm = ''
  stack_position_start = len((flatten(STACK_FRAMES[-1]['vars'][:LOOP_IDS[-1][1]])))
  stack_position_end = len((flatten(STACK_FRAMES[-1]['vars'])))
  # free first
  for i in range(stack_position_start, stack_position_end):
    if flatten(STACK_FRAMES[-1]['vars'])[i][1] == 'STRING':
      asm += assembly.GET_LOCAL_VARIABLE.format(4 + i * 4)
      asm += assembly.PUSH_RESULT
      asm += assembly.EXT_FREE_STR
  # then pop
  for i in range(stack_position_start, stack_position_end):
    asm += assembly.POP_LOCAL_VARIABLE

  return asm


def free_arguments(args, arg_types):
  # if the argument is a function call, that returns a string
  # we need to free the string after the function call
  # because it has no other owner
  asm = ''
  for i, arg in enumerate(args):
    if arg_types[i] == 'STRING' and type(arg) == list:
      asm += assembly.EXT_FREE_STR
      # (this adds 4 to esp already, clearing the stack)
    else:
      # -> improve
      asm += assembly.CLEAR_STACK.format(4)
  return asm


### parser

def parse_param_str(param_str):

  """parse a parameter string of the form:

  '[ <name>:<type> [, <name>:<type>]* ]'

  into a list of parameters, e.g.:

  [ [ "a", "INT" ], [ "b", "INT" ] ]

  """

  param_str = param_str.strip()[1:-1]

  if param_str == '':
    return []

  params = []
  for param in param_str.split(','):
    [ name, _type ] = param.split(':')
    params.append([ name.strip(), _type.strip() ])

  return params


def parse_array_str(array_str):

  """parse an array string of the form:

  '[ <expr> [, <expr>]* ]'

  into a list of expressions, e.g.:

  [ "1", "2", "3" ]
  """
  array_str = array_str.strip()[1:-1]

  if array_str == '':
    return []

  split_argstr = get_split_argstr(array_str)

  array = []
  for arg in split_argstr:
    if arg.lstrip().startswith('{'):
      sys.exit("Error: block in array not supported: %s" % arg)
    else:
      array.append(arg)

  return array


def parse(expr):

  """parse an expression of the form:

  <kw> ( <expr> [, <expr>]* )

  into a list of keyword and arguments, e.g.:

  [ "fn", [ "1", "2" ] ]
  [ "fn", [ "1", [ "add", [ "2", "3" ] ], [ "sub", [ "4", "5" ] ] ] ]

  """

  if '(' not in expr and ')' not in expr:
    return expr.strip()

  if expr.startswith('[') and expr.endswith(']'):
    return expr

  [ kw, argstr ] = get_kwargstr(expr)

  split_argstr = get_split_argstr(argstr)

  args = []
  for arg in split_argstr:
    if arg.lstrip().startswith('{'):
      args.append(arg)
    else:
      args.append(parse(arg))

  return [ kw, args ]


### eval

def eval_block(block, asm, depth):

  """evaluate a block of expressions of the form:

  '{ <expr> [, <expr>]* }'

  it creates and destroys a new scope for local variables

  """

  if not block.startswith('{') or not block.endswith('}'):
    sys.exit("Error: block does not start and end with curly braces: %s" % block)

  STACK_FRAMES[-1]['vars'].append([])

  block_exprs = split_expressions(block.strip()[1:-1])
  for expr in block_exprs:
    [ asm, _type ] = eval(parse(expr), asm, depth + 1)

  # if the block was a function scope, we wouldn't actually have to pop
  # the variables here, because the stack frame takes care of that
  # but we want to free the memory of the variables in the block

  # free variables in the current block
  offset = len(flatten(STACK_FRAMES[-1]['vars'][0:-1])) * 4
  for i, var in enumerate(STACK_FRAMES[-1]['vars'][-1]):
    if TYPES[var[1]]['has_memory']:
      TYPES[var[1]]['free_function'](asm, i)
      # asm += assembly.GET_LOCAL_VARIABLE.format(4 + offset + i * 4)
      # asm += assembly.PUSH_RESULT
      # asm += assembly.EXT_FREE_STR

  # -> this could be improved to use something like:
  #    add esp, 4 * len(STACK_FRAMES[-1]['vars'][-1])
  for var in STACK_FRAMES[-1]['vars'][-1]:
    asm += assembly.POP_LOCAL_VARIABLE

  STACK_FRAMES[-1]['vars'].pop()

  return asm


def eval_str(expr, asm, depth = 0):

  if expr == '': return [ asm, 'UNDEF' ]

  # check for variable
  [ stack_pos, _type ] = find_variable(expr, STACK_FRAMES[-1]['vars'])

  if stack_pos is not None:
    asm += assembly.GET_LOCAL_VARIABLE.format(4 + stack_pos * 4)
    return [ asm, _type ]

  # check for parameter
  [ stack_pos, _type ] = find_parameter(expr, STACK_FRAMES[-1]['params'])

  if stack_pos is not None:
    asm += assembly.GET_PARAMETER.format(8 + stack_pos * 4)
    return [ asm, _type ]

  if expr.isdigit():
    asm += assembly.LITERAL.format(expr)
    return [ asm, 'INT' ]

  # negative numbers
  if expr.startswith('-') and expr[1:].isdigit():
    asm += assembly.LITERAL.format(expr)
    return [ asm, 'INT' ]

  if expr.startswith("'") and expr.endswith("'"):
    # add literal to text section/literals
    str_id = 'string_' + str(get_unique_count())
    LITERALS.append(assembly.DATA_STRING.format(str_id, expr[1:-1]))

    asm += assembly.LITERAL.format(str_id)
    return [ asm, 'STRING_LIT' ]

  if expr.startswith('[') and expr.endswith(']'):
    # print(expr)
    array_values = parse_array_str(expr)
    # print(array_values)
    asm += assembly.LITERAL.format(len(array_values))
    asm += assembly.PUSH_RESULT
    asm += assembly.CALL_EXTENSION.format('Array_new')
    asm += assembly.CLEAR_STACK.format(4)
    asm += assembly.PUSH_RESULT

    for i, value in enumerate(array_values):
      # -> if it's a variable pointing to a string or array,
      #    we need to set the type to UNDEF to avoid freeing it twice
      [ asm, _type ] = eval(parse(value), asm, depth + 1)
      asm += assembly.PUSH_RESULT
      asm += assembly.LITERAL.format(TYPES[_type]['enum'])
      asm += assembly.PUSH_RESULT
      asm += assembly.LITERAL.format(i)
      asm += assembly.PUSH_RESULT
      asm += assembly.CALL_EXTENSION.format('put')
      asm += assembly.CLEAR_STACK.format(4 * 3)

    asm += assembly.POP_LOCAL_VARIABLE
    #asm += assembly.CLEAR_STACK.format(4)

    return [ asm, 'ARRAY' ]

  sys.exit("Error: unknown variable or literal: " + expr)


def eval(expr, asm, depth = 0):

  """evaluate an expression of the form:

  <kw | func> ( <expr> [, <expr>]* )

  """

  # 1) first we check if the expression is a string,
  #    if it is, it can be:
  #
  # 1. a SYMBOL of a variable or a parameter
  #             these are allocated on the stack, so we find
  #             the stack position and load the value into the
  #             return register
  # 2. a DIGIT, currently this can be a positive or negative integer
  #             we put the value into the return register
  # 3. a STRING, a string literal, we add the string to the text section
  #             and put the address into the return register

  if type(expr) == str:
    return eval_str(expr, asm, depth)

  # at this point we know we have an expression

  [ kw, args ] = expr

  # 2) first we handle cases, where the arguments need some special handling
  #    e.g. var takes a variable name and an expression, but if we parse the
  #    variable name now it would result in an error, because it is not yet
  #    defined
  # -> idea: we could use a string for the variable names and then parse them
  # regularly, (but this would be a bit ugly <-- this is what copilot thinks)

  if kw == "var":
    check_arguments(args, 2, 'var')

    # check that variable name starts with a letter
    if not args[0][0].isalpha():
      sys.exit("Error: variable name must start with a letter")

    # check redeclaration
    for var in STACK_FRAMES[-1]['vars'][-1]:
      if var[0] == args[0]:
        sys.exit("Redeclaration Error: '" + args[0] + "'")

    check_redeclaration_parameter(args)

    # evaluate the 2nd argument
    [ asm, _type ] = eval(args[1], asm, depth + 1)
    asm += assembly.PUSH_RESULT

    if _type == 'UNDEF':
      sys.exit("Error: invalid type: '" + _type + "'" + " for variable: '" + args[0] + "'")

    move_ownership(args[1], _type)

    # store variable in compiler stack
    STACK_FRAMES[-1]['vars'][-1].append([ args[0], _type ])

    return [ asm, 'UNDEF' ]

  if kw == 'set':
    check_arguments(args, 2, 'set')

    [ stack_pos, vtype ] = find_variable(args[0], STACK_FRAMES[-1]['vars'])
    if stack_pos is None:
      sys.exit("Error setting undeclared variable: '" + args[0] + "'")

    check_redeclaration_parameter(args)

    # evaluate the 2nd argument
    [ asm, _type ] = eval(args[1], asm, depth + 1)
    asm += assembly.PUSH_RESULT

    if _type != vtype:
      sys.exit("Error: Type mismatch variable: '" + args[0] + "'" + " expected: '" \
        + vtype + "'" + " got: '" + _type + "'")

    # same as for var above
    move_ownership(args[1], _type)

    # this will consume the value on the stack top
    # and update the variable in the correct stack location
    asm += assembly.PRIMARIES[kw].format(4 + stack_pos * 4)

    return [ asm, 'UNDEF' ]

  if kw == 'block':
    asm = eval_block(args[0], asm, depth)
    return [ asm, 'BLOCK' ]

  if kw == 'if':
    # get id for block
    id = get_unique_count()

    # eval condition
    [ asm, _type ] = eval(args[0], asm, depth + 1)
    asm += assembly.PUSH_RESULT

    if _type != 'INT':
      sys.exit("Error: if condition must be of type INT: '" + expr + "'")

    asm += assembly.IF_START.format(id)

    asm = eval_block(args[1], asm, depth)

    if len(args) == 3:
      asm += assembly.ELSE_START.format(id)

      asm = eval_block(args[2], asm, depth)

    else:
      asm += assembly.ELSE_START.format(id)

    asm += assembly.IF_END.format(id)

    return [ asm, 'BLOCK' ]

  if kw == 'while':
    # get id for block
    id = get_unique_count()

    asm += assembly.WHILE_START.format(id)

    # eval condition
    [ asm, _type ] = eval(args[0], asm, depth + 1)
    asm += assembly.PUSH_RESULT

    if _type != 'INT':
      sys.exit("Error: while condition must be of type INT: '" + expr + "'")

    # emit condition evaluation
    asm += assembly.WHILE_CONDITION_EVAL.format(id)

    LOOP_IDS.append([ id, len(STACK_FRAMES[-1]['vars']) ])
    asm = eval_block(args[1], asm, depth)
    LOOP_IDS.pop()

    asm += assembly.WHILE_END.format(id)

    return [ asm, 'BLOCK' ]

  if kw == 'function':
    check_arguments(args, 4, 'function')

    # check that function name starts with a letter
    if not args[0][0].isalpha():
      sys.exit("Error: function name must start with a letter")

    params = parse_param_str(args[1])

    for param in params:
      # check that parameter names start with a letter
      if not param[0][0].isalpha():
        sys.exit("Error: parameter name must start with a letter")

      # check type declaration
      if param[1] not in TYPES:
        sys.exit("Error: unknown type: '" + param[1] + "'" + " for parameter: '" + param[0] + "'")

    # check return type
    if args[2] not in TYPES:
      sys.exit("Error: unknown type: '" + args[2] + "'" + " for function: '" + args[0] + "'")

    FUNCTIONS[args[0]] = {
      'param_types': [ x[1] for x in params ],
      'return_type': args[2],
      'asm': ''
    }

    # push a new frame onto the stack_frames
    STACK_FRAMES.append({
      'name': args[0],
      'params': [ x for x in params ],
      'vars': [],
      'return_type': args[2]
    })

    fn_asm = ""
    fn_asm += assembly.FUNCTION_START.format(args[0])

    fn_asm = eval_block(args[3], fn_asm, 0)

    fn_asm += assembly.FUNCTION_END.format(args[0])

    FUNCTIONS[args[0]]['asm'] = fn_asm

    STACK_FRAMES.pop()

    return [ asm, args[2] ]

  if kw == "return":
    rtype = STACK_FRAMES[-1]['return_type']
    fname = STACK_FRAMES[-1]['name']

    if (rtype == 'UNDEF' and len(args) != 0) or \
       (rtype != 'UNDEF' and len(args) == 0) or \
        len(args) > 1:
      sys.exit("Error: Wrong number of arguments for return: '" + fname + "'")

    # variables that have memory allocated should be freed here
    # except for the return value
    # (this has to be done before the argument evaluation)
    for i, var in enumerate(flatten(STACK_FRAMES[-1]['vars'])):
      if TYPES[var[1]]['has_memory'] and var[0] != args[0]:
        TYPES[var[1]]['free_function'](asm, i)

    if len(args) > 0:
      [ asm, _type ] = eval(args[0], asm, depth + 1)
      # we want to use eax as the return register, not the stack
      #asm += assembly.PUSH_RESULT

      if _type != rtype:
        sys.exit("Error: expected type " + rtype + " for return, got " + _type + ":\n'" \
          + "function: " + fname + ", arg: " + args[0] + "'")

    asm += assembly.PRIMARIES[kw]

    return [ asm, rtype ]

  # 3) now we handle the remaining cases where all arguments
  #    can be evaluated and pushed onto the stack

  arg_types = []
  for arg in reversed(args):
    [ asm, _type ] = eval(arg, asm, depth + 1)
    asm += assembly.PUSH_RESULT

    arg_types.append(_type)

  rtype = 'UNDEF'

  if kw == "exit":
    if len(args) == 0:
      asm += assembly.LITERAL.format(0)
      asm += assembly.PUSH_RESULT
    else:
      check_arg_types(kw, arg_types, ['INT'])

    # -> free all allocated variables
    # -> ommitting this for now because it is not really necessary

    asm += assembly.PRIMARIES[kw]

  elif kw in EXTENSIONS:
    check_arg_types(kw, arg_types, EXTENSIONS[kw]['arg_types'])
    asm += assembly.CALL_EXTENSION.format(kw)
    asm += free_arguments(args, arg_types)
    if 'return_type' in EXTENSIONS[kw]:
      rtype = EXTENSIONS[kw]['return_type']

  elif kw == 'inc' or kw == 'dec':
    check_arg_types(kw, arg_types, [ 'INT' ])

    [ stack_pos, _type ] = find_variable(args[0], STACK_FRAMES[-1]['vars'])
    if stack_pos is None:
      sys.exit("Error in inc/dec: variable '" + args[0] + "' not found")

    asm += assembly.PRIMARIES[kw].format(4 + stack_pos * 4)

  elif kw in assembly.UNARIES:
    check_arg_types(kw, arg_types, [ 'INT' ])

    asm += assembly.UNARIES[kw]
    rtype = 'INT'

  elif kw in assembly.BINARIES:
    check_arg_types(kw, arg_types, [ 'INT', 'INT' ])

    asm += assembly.BINARIES[kw]
    rtype = 'INT'

  elif kw in assembly.COMPARISONS:
    check_arg_types(kw, arg_types, [ 'INT', 'INT' ])

    asm += assembly.COMPARISONS[kw].format(get_unique_count())
    rtype = 'INT'

  elif kw in assembly.LOGICALS:
    if kw == 'not':
      check_arg_types(kw, arg_types, [ 'INT' ])
    else:
      check_arg_types(kw, arg_types, [ 'INT', 'INT' ])

    asm += assembly.LOGICALS[kw].format(get_unique_count())
    rtype = 'INT'

  elif kw == 'check_overflow':
    check_arg_types(kw, arg_types, [])
    id = get_unique_count()
    asm += assembly.CHECK_OVERFLOW.format(id)
    rtype = 'INT'

  elif kw == 'break':
    check_arg_types(kw, arg_types, [])

    asm += free_at_loop_break()

    asm += assembly.WHILE_BREAK.format(LOOP_IDS[-1][0])

  elif kw == 'continue':
    check_arg_types(kw, arg_types, [])

    asm += free_at_loop_break()

    asm += assembly.WHILE_CONTINUE.format(LOOP_IDS[-1][0])

  elif kw in FUNCTIONS:
    check_arg_types(kw, arg_types, FUNCTIONS[kw]['param_types'])
    asm += assembly.FUNCTION_CALL.format(kw, len(args) * 4)

    asm += free_arguments(args, arg_types)

    rtype = FUNCTIONS[kw]['return_type']

  else:
    sys.exit("Error: unknown keyword '" + kw + "'")

  return [ asm, rtype ]


### main

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
    [ main_asm, _type ] = eval(expr, main_asm)

  fn_asm = ''
  for fn in FUNCTIONS:
    fn_asm += FUNCTIONS[fn]['asm']

  # -> free all allocated variables at the end of the program
  # -> ommitting this for now because it is not really necessary

  # combine main assembly code with header, built-in functions and footer
  out = assembly.HEAD.format(START_LABEL) \
    + assembly.DATA \
    + ''.join(LITERALS) \
    + assembly.TEXT \
    + assembly.EXIT \
    + fn_asm \
    + assembly.START.format(START_LABEL) \
    + main_asm + assembly.DEFAULT_EXIT

  # write to output file
  with open(OUTFILE, 'w') as f:
    f.write(out)


# run main function
if __name__ == '__main__':
  main()
