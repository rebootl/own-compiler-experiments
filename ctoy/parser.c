
#include <stdio.h>
#include <stdlib.h> // exit
#include <stdbool.h>

#include "scanner.h"
#include "parser.h"

typedef struct {
  Token current;
  Token previous;
	bool hadError;
} Parser;

Parser parser;

// Token currentToken;

static void advance() {
  parser.previous = parser.current;
  parser.current = scanToken();
}

static void consume(TokenType type, const char* message) {
  if (parser.current.type == type) {
    advance();
    return;
  }

	// -> improve error handling
  printf("Error: %s\n", message);
  parser.hadError = true;
}

static int getPrecedence(TokenType type) {
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
void parse(int precedence);

static int prefix_handler() {

	// TokenType type = parser.previous.type;

	switch (parser.previous.type) {
    case TOKEN_INT:
      printf("INT: %.*s\n", parser.previous.length, parser.previous.start);
      return 1;
    case TOKEN_MINUS:
			parse(70);
      printf("SIGN MINUS\n");
      return 1;
    default:
      printf("Error: expected expression\n");
      return 0;
  }
}

static int infix_handler() {
	// save the token here for later
	TokenType type = parser.previous.type;

	// recurse
  parse(getPrecedence(type));

  switch (type) {
    case TOKEN_PLUS:
      printf("PLUS\n");
      return 1;
    case TOKEN_MINUS:
      printf("MINUS\n");
      return 1;
    case TOKEN_STAR:
      printf("STAR\n");
      return 1;
    case TOKEN_SLASH:
      printf("SLASH\n");
      return 1;
    default:
      printf("Error: expected expression infix\n");
      return 0;
  }
}

// -> static
void parse(int precedence) {

	advance();
	int success = prefix_handler();
	if (!success) {
    printf("error: prefix_handler\n");
    return;
  }

	while (precedence <= getPrecedence(parser.current.type)) {
		// printf("precedence: %d\n", precedence);
    
		advance();
		success = infix_handler();
		if (!success) {
      printf("error: infix_handler\n");
      return;
    }
  }

	// printf("done\n");
}

void interpret(char *source) {
  initScanner(source);

	parser.hadError = false;

	advance();
	parse(0);
	consume(TOKEN_EOF, "Expected end of expression");

	/*
	while (1) {
    Token token = scanToken();

    if (token.type == TOKEN_EOF) break;

    printf("token type: %d\n", token.type);
		printf("token: \"%.*s\"\n", token.length, token.start);

  }
	*/

}

