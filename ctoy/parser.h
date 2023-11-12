
#ifndef parser_h
#define parser_h

#include "../extends/extensions.h"

typedef enum {
	OP_LITERAL,
	OP_ADD,
	OP_SUBTRACT,
	OP_MULTIPLY,
	OP_DIVIDE,
	OP_NEGATE,
} OpCode;

typedef struct {
  int count;
  int capacity;
	int *ops;
} ByteCode;

typedef struct {
	Element *literals;
	ByteCode *bytecode;
} ParserResult;

// void parse(int precedence);
void interpret(char* source);

#endif /* parser_h */
