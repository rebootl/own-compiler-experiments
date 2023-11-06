
#include <stdio.h>
#include <stdlib.h> // exit
#include <string.h> // strncpy

#include "scanner.h"
#include "parser.h"

#include "../extends/extensions.h"

typedef struct {
  Token current;
  Token previous;
	int had_error;
  char* error_message;
} Parser;

Parser parser;
ParserResult parser_result;

ByteCode* new_ByteCode(int capacity) {
  ByteCode* bytecode = _alloc(sizeof(ByteCode));
  bytecode->count = 0;
  bytecode->capacity = capacity == 0 ? 8 : capacity;
  bytecode->op = _alloc(sizeof(OpCode) * capacity);
  return bytecode;
}

void emit(OpCode op) {
  ByteCode* bc = parser_result.bytecode;
  if (bc->count == bc->capacity) {
    bc->capacity *= 2;
    bc->op = _realloc(bc->op, sizeof(OpCode) * bc->capacity);
  }
  bc->op[bc->count++] = op;
}

void print_bytecode() {
  ByteCode* bc = parser_result.bytecode;
  for (int i = 0; i < bc->count; i++) {
    // printf("%d\n", bc->op[i]);
    switch (bc->op[i]) {
      case OP_LITERAL:
        printf("OP_LITERAL %d\n", bc->op[++i]);
        break;
      case OP_ADD:
        printf("OP_ADD\n");
        break;
      case OP_SUBTRACT:
        printf("OP_SUBTRACT\n");
        break;
      case OP_MULTIPLY:
        printf("OP_MULTIPLY\n");
        break;
      case OP_DIVIDE:
        printf("OP_DIVIDE\n");
        break;
      case OP_NEGATE:
        printf("OP_NEGATE\n");
        break;
      default:
        printf("OP_UNKNOWN\n");
        break;
    }
  }
}

static int parse_int(const char* start, int length) {
  char* int_str = malloc(length + 1);
  strncpy(int_str, start, length);
  int_str[length] = '\0';
  int int_val = atoi(int_str);
  free(int_str);
  return int_val;
}

static void error(char* message) {
  if (parser.had_error) {
    return;
  }

  parser.error_message = message;
  parser.had_error = 1;
}

static void advance() {
  parser.previous = parser.current;
  parser.current = scan_token();
  if (parser.current.type == TOKEN_ERROR) {
    error("Error: unexpected character\n");
  }
}

static void consume(TokenType type, char* message) {
  if (parser.current.type == type) {
    advance();
    return;
  }

  error(message);
}

static int get_precedence(TokenType type) {
  switch (type) {
    case TOKEN_PLUS:
    case TOKEN_MINUS:
      return 50;
    case TOKEN_STAR:
    case TOKEN_SLASH:
      return 60;
    default:
      return -1;
  }
}

// forward declaration
static void parse_expression(int precedence);

static void prefix_handler() {
  int int_val;
  int int_idx;

	switch (parser.previous.type) {
    case TOKEN_INT:
      int_val = parse_int(parser.previous.start, parser.previous.length);
      int_idx = append(parser_result.literals, new_Int(int_val));
      // -> emit byte code
      // INT idx
      emit(OP_LITERAL);
      emit(int_idx);
      
      printf("INT: %.*s\n", parser.previous.length, parser.previous.start);
      break;
    case TOKEN_MINUS:
			parse_expression(70);
      emit(OP_NEGATE);
      printf("SIGN MINUS\n");
      break;
    case TOKEN_LEFT_PAREN:
      parse_expression(0);
      consume(TOKEN_RIGHT_PAREN, "Error: expected right paren\n");
      break;
    default:
      error("Error: expected prefix token\n");
  }
}

static void infix_handler() {
	// save the token here for later
	TokenType type = parser.previous.type;

	// recurse
  parse_expression(get_precedence(type));

  switch (type) {
    case TOKEN_PLUS:
      printf("PLUS\n");
      emit(OP_ADD);
      break;
    case TOKEN_MINUS:
      printf("MINUS\n");
      emit(OP_SUBTRACT);
      break;
    case TOKEN_STAR:
      printf("STAR\n");
      emit(OP_MULTIPLY);
      break;
    case TOKEN_SLASH:
      printf("SLASH\n");
      emit(OP_DIVIDE);
      break;
    default:
      error("Error: expected infix token\n");
  }
}

static void parse_expression(int precedence) {

	advance();
	prefix_handler();
	// if (parser.had_error) {
 //    return;
 //  }

	while (precedence <= get_precedence(parser.current.type)) {
		advance();
		infix_handler();
		// if (parser.had_error) {
  //     return;
  //   }
  }

}

void interpret(char *source) {
  init_scanner(source);

	parser.had_error = 0;
  parser_result.literals = new_Array(0);
  parser_result.bytecode = new_ByteCode(0);

	advance();
  if (parser.current.type == TOKEN_EOF) {
    return;
  }

	parse_expression(0);
	consume(TOKEN_EOF, "Error: expected end of expression\n");

  if (parser.had_error) {
    printf("%s", parser.error_message);
  }
  // print size
  printf("sizeof: %lu\n", sizeof(long long int));
  
  printf("ByteCode:\n");
  print_bytecode();
  printf("Literals: ");
  print(parser_result.literals);
  printf("\n");
	/*
	while (1) {
    Token token = scanToken();

    if (token.type == TOKEN_EOF) break;

    printf("token type: %d\n", token.type);
		printf("token: \"%.*s\"\n", token.length, token.start);

  }
	*/

}

