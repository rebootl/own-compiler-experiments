
#include <stdio.h>
#include <stdlib.h> // exit

#include "scanner.h"
#include "parser.h"

typedef struct {
  Token current;
  Token previous;
	int had_error;
  char* error_message;
} Parser;

Parser parser;

void error(char* message) {
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

	switch (parser.previous.type) {
    case TOKEN_INT:
      printf("INT: %.*s\n", parser.previous.length, parser.previous.start);
      break;
    case TOKEN_MINUS:
			parse_expression(70);
      printf("SIGN MINUS\n");
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
      break;
    case TOKEN_MINUS:
      printf("MINUS\n");
      break;
    case TOKEN_STAR:
      printf("STAR\n");
      break;
    case TOKEN_SLASH:
      printf("SLASH\n");
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


	advance();
  if (parser.current.type == TOKEN_EOF) {
    return;
  }

	parse_expression(0);
	consume(TOKEN_EOF, "Error: expected end of expression\n");

  if (parser.had_error) {
    printf("%s", parser.error_message);
  }

	/*
	while (1) {
    Token token = scanToken();

    if (token.type == TOKEN_EOF) break;

    printf("token type: %d\n", token.type);
		printf("token: \"%.*s\"\n", token.length, token.start);

  }
	*/

}

