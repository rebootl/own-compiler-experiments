

A toy compiler for a toy language, for learning purposes.


## Resources:

* Crafting Interpreters: https://craftinginterpreters.com/

* An Incremental Approach to Compiler Construction: http://scheme2006.cs.uchicago.edu/11-ghuloum.pdf


## Language grammar:

```
PROGRAM   : [ EXPRESSION ]*          # n expressions

COMMENT   : <COMMENT_CHAR> + <comment> + "\n"

PRIMARY   : print( EXPRESSION ) |
            println( EXPRESSION | <empty> ) |
            exit( EXPRESSION Default: 0 ) |
            var( VARIABLE, EXPRESSION ) |
            set( VARIABLE, EXPRESSION ) |
            inc( VARIABLE ) | dec( VARIABLE )

BINARY    : add( EXPRESSION, EXPRESSION ) |
            sub( EXPRESSION, EXPRESSION ) |
            mul( EXPRESSION, EXPRESSION ) |
            div( EXPRESSION, EXPRESSION )

EXPRESSION: PRIMARY | VARIABLE | LITERAL |
            BINARY |
            COMPARISON | LOGICAL

VARIABLE  : <variable name>

LITERAL   : <unsigned integer>

COMPARISON: eq( EXPRESSION, EXPRESSION ) |
            ne( EXPRESSION, EXPRESSION ) |
            lt( EXPRESSION, EXPRESSION ) |
            gt( EXPRESSION, EXPRESSION ) |
            le( EXPRESSION, EXPRESSION ) |
            ge( EXPRESSION, EXPRESSION )

LOGICAL   : and( EXPRESSION, EXPRESSION ) |
            or( EXPRESSION, EXPRESSION ) |
            not( EXPRESSION )

BLOCK     : "{" PROGRAM "}"

CONDITION : if( EXPRESSION, BLOCK, [ BLOCK ]) |

LOOP      : while( EXPRESSION, BLOCK )

FUNCTION  : function(
              <function name>,
              "[" <function arguments, comma separated> "]",
              BLOCK
            )

CONTROL   : return( EXPRESSION )      # allowed inside a function
            break() | continue()      # allowed inside a loop

FUNCTION_CALL: <function name>( EXPRESSION, [ EXPRESSION ]* )

```
