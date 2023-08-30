def split_list_str(list_str):

  """split an inline list of the form:

  '<LITERAL> [, <LITERAL>]*'

  into a list of elements, e.g.:

  [ "1", "2" ], [ "1", [ "2", "3" ] ],
  [ a, b ], [ a, [ b, c ] ], etc.

  """

  list_str = list_str.strip()

  split_list = []
  arg = ''
  depth = 0

  for c in _list:
    if c == '[':
      depth += 1
    elif c == ']':
      depth -= 1
    elif c == ',' and depth == 0:
      split_list.append(arg.strip())
      arg = ''
      continue

    arg += c

  if depth != 0:
    sys.exit("Error: unbalanced square brackets in list: %s" % list_str)

  if arg != '':
    split_list.append(arg.strip())

  return split_list


def parse_list(_list):

  """parse an inline list of the form:

  '[ <expr> [, <expr>]* ]'

  into a list of elements, e.g.:

  [ "1", "2" ]

  """
  if '[' not in _list and ']' not in _list:
    sys.exit("Error: expected list, got: " + _list)

  _list = _list.strip()[1:-1]

  split_list = split_list_str(_list)

  args = []
  for arg in split_list:
    if arg.lstrip().startswith('['):
      args.append(parse_list(arg))
    else:
      args.append(arg)

  return args
