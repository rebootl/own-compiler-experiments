

A toy compiler for a toy language, for learning purposes.


## Resources:




## Language grammar:

```
PROGRAM   : <empty> | PRIMARY | UNARY | BINARY

PRIMARY   : print( EXPRESSION ) | println() |
            exit( EXPRESSION Default: 0 ) |
            var( VARIABLE, EXPRESSION ) |
            set( VARIABLE, EXPRESSION )

UNARY     : inc( VARIABLE ) | dec( VARIABLE )

BINARY    : add( EXPRESSION, EXPRESSION ) | 
            sub( EXPRESSION, EXPRESSION )

EXPRESSION: VARIABLE | LITERAL |
            BINARY | UNARY |
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

BLOCK     : block:
              PROGRAM

```
