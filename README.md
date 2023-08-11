

A toy compiler for a toy language, for learning purposes.


## Resources:

* Crafting Interpreters: https://craftinginterpreters.com/

* An Incremental Approach to Compiler Construction: http://scheme2006.cs.uchicago.edu/11-ghuloum.pdf


## Language grammar:

```
PROGRAM   : "" | "\n" | <indent of block> + LINE

LINE      : "" | PRIMARY | BINARY |
            BLOCK | COMMENT + "\n"

COMMENT   : <COMMENT_CHAR> + <comment> + "\n"

PRIMARY   : print( EXPRESSION ) | println() |
            exit( EXPRESSION Default: 0 ) |
            var( VARIABLE, EXPRESSION ) |
            set( VARIABLE, EXPRESSION ) |
            inc( VARIABLE ) | dec( VARIABLE )

BINARY    : add( EXPRESSION, EXPRESSION ) | 
            sub( EXPRESSION, EXPRESSION )

EXPRESSION: VARIABLE | LITERAL |
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

BLOCK     : block:
            <indent of block> + PROGRAM

```
