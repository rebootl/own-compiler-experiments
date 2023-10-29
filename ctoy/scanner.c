/*

scan a string and turn it into tokens

code partially (mostly:) based on https://github.com/munificent/craftinginterpreters/

Copyright (c) 2015 Robert Nystrom

*/

#include <stdio.h>
#include <stdlib.h>

char test_str[100] = "10 + 2 - 3";

typedef struct {
  const char* start;
  const char* current;
} Scanner;

Scanner scanner;

typedef enum {
  TOKEN_INT,
  TOKEN_PLUS,
	TOKEN_MINUS,
	TOKEN_STAR,
	TOKEN_SLASH,
	TOKEN_EOF,
} TokenType;

typedef struct {
  TokenType type;
  const char* start;
  int length;
} Token;


static Token makeToken(TokenType type) {
  Token token;
  token.type = type;
  token.start = scanner.start;
  token.length = (int)(scanner.current - scanner.start);
  return token;
}


void initScanner(const char* source) {
  scanner.start = source;
  scanner.current = source;
}

static char advance() {
  scanner.current++;
  return scanner.current[-1];
}

static char peek() {
  return *scanner.current;
}

static void skipWhitespace() {
  for (;;) {
    char c = peek();
    switch (c) {
      case ' ':
      case '\r':
      case '\t':
      case '\n':
        advance();
        break;
      default:
        return;
    }
  }
}

Token scanToken() {
  skipWhitespace();
	scanner.start = scanner.current;

  if (*scanner.current == '\0') return makeToken(TOKEN_EOF);

  char c = advance();
 
	if (c >= '0' && c <= '9') {
    while (peek() >= '0' && peek() <= '9') advance();
    return makeToken(TOKEN_INT);
  }

  switch (c) {
    case '+': return makeToken(TOKEN_PLUS);
		case '-': return makeToken(TOKEN_MINUS);
		case '*': return makeToken(TOKEN_STAR);
		case '/': return makeToken(TOKEN_SLASH);
  }
	
  printf("error: unexpected character.\n");
	exit(1);
}


int main(int argc, char** argv) {

  initScanner(test_str);

	while (1) {
	  Token token = scanToken();

	  printf("token type: %d\n", token.type);
		printf("token: \"%.*s\"\n", token.length, token.start);

		if (token.type == TOKEN_EOF) break;
  }

  return 0;
}

