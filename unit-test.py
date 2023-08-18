#!/usr/bin/env python
#
# 

from compiler import parse, split_expressions

EXPRESSIONS = [
  [ "", "" ],
  [ "a", "a" ],
  [ "abc", "abc" ],
  [ "1", "1" ],
  [ "123", "123" ],
  [ "fn()", [ "fn", [] ] ],
  [ "fn ( )", [ "fn", [] ] ],
  [ "fn (  )", [ "fn", [] ] ],
  [ "fn(1)", [ "fn", [ "1" ] ] ],
  [ "fn (1)", [ "fn", [ "1" ] ] ],
  [ "fn ( 1 )", [ "fn", [ "1" ] ] ],
  [ "fn(1, 2)", [ "fn", [ "1", "2" ] ] ],
  [ "fn(1, fn(2))", [ "fn", [ "1", [ "fn", [ "2" ] ] ] ] ],
  [ "fn( 1, add(2, 3) )", [ "fn", [ "1", [ "add", [ "2", "3" ] ] ] ] ],
  [ "add(1, 2, 3)", [ "add", [ "1", "2", "3" ] ] ],
  [ "add(1, 2, 3, 4)", [ "add", [ "1", "2", "3", "4" ] ] ],
  [ "add (1, 2, 3, 4)", [ "add", [ "1", "2", "3", "4" ] ] ],
  [ "add (1, add ( 2, 3 ), 4)", [ "add", [ "1", [ "add", [ "2", "3" ] ], "4" ] ] ],
  [ "add (1, add ( 2, 3 ), sub ( 4, 5 ) )", [ "add", [ "1", [ "add", [ "2", "3" ] ], [ "sub", [ "4", "5" ] ] ] ] ],
  [ """add (
    1,
    add ( 2, 3 ),
    sub ( 4, 5 )
  )""", [ "add", [ "1", [ "add", [ "2", "3" ] ], [ "sub", [ "4", "5" ] ] ] ] ],
  [ """add(
    1,
    add (
      2,    ; comment
      3     ; comment
    ),
    sub (
      4,
      5
    )
  )""", [ "add", [ "1", [ "add", [ "2", "3" ] ], [ "sub", [ "4", "5" ] ] ] ] ],
]


PROGRAMS = [
  [ "", [] ],
  [ "a", [ "a" ] ],
  [ "abc", [ "abc" ] ],
  [ "1", [ "1" ] ],
  [ "123", [ "123" ] ],
  [ "fn()", [ "fn()" ] ],
  [ "fn ( )", [ "fn()" ] ],
  [ "fn (  )", [ "fn()" ] ],
  [ "fn(1) fn(2, 3)", [ "fn(1)", "fn(2,3)" ] ],
  [ "fn (1) fn (2, 3)", [ "fn(1)", "fn(2,3)" ] ],
  [ "fn ( 1 ) add ( 2, 3 )", [ "fn(1)", "add(2,3)" ] ],
  [ "fn(1, 2) sub(3, 4)", [ "fn(1,2)", "sub(3,4)" ] ],
  [ "fn(1, fn(2)) fn(3, 4)", [ "fn(1,fn(2))", "fn(3,4)" ] ],
  [ """fn( 1, add(2, 3) )
  fn(4, 5)""", [ "fn(1,add(2,3))", "fn(4,5)" ] ],
  [ """fn( 1, add(2, 3) )
  fn(4, 5)
  """, [ "fn(1,add(2,3))", "fn(4,5)" ] ],
  [ """; comment
fn( 1, add(2, 3) )

  add(
    1,
    2          ; comment
  )

  fn(4, 5)
  """, [ "fn(1,add(2,3))", "add(1,2)", "fn(4,5)" ] ],
  [ """

; comment

fn( 1, add(2, 3) )

add(
  1,
  2          ; comment
)

""", [ "fn(1,add(2,3))", "add(1,2)" ] ],
]


def test_get_kwargs():
  
  for expr in EXPRESSIONS:
    #print("Testing: %s" % expr[0])
    try:
      assert parse(expr[0]) == expr[1], \
        "parse(%s) should be %s but got %s" % (expr[0], expr[1], parse(expr[0]))
    except AssertionError as e:
      print(e)
      return
  
  print("get_kwargs() tests passed!")


def test_split_expressions():
    
  for program in PROGRAMS:
    #print("Testing: %s" % program[0])
    try:
      assert split_expressions(program[0]) == program[1], \
        "split_expressions(%s) should be %s but got %s" % (program[0], program[1], split_expressions(program[0]))
    except AssertionError as e:
      print(e)
      return
  
  print("split_expressions() tests passed!")

if __name__ == "__main__":
  test_get_kwargs()
  test_split_expressions()