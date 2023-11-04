/*

scan source code string and turn it into tokens

*/

#include <stdio.h>
#include <stdlib.h> // exit

#include "scanner.h"

char test_str[100] = "10 + 2 - 3";

typedef struct {
  const char* start;
  const char* current;
} Scanner;

Scanner scanner;


void init_scanner(const char* source) {
  scanner.start = source;
  scanner.current = source;
}

static Token make_token(TokenType type) {
  Token token;
  token.type = type;
  token.start = scanner.start;
  token.length = (int)(scanner.current - scanner.start);
  return token;
}

static char advance() {
  scanner.current++;
  return scanner.current[-1];
}

static char peek() {
  return *scanner.current;
}

static void skip_whitespace() {
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

Token scan_token() {
  skip_whitespace();
	scanner.start = scanner.current;

  if (*scanner.current == '\0') return make_token(TOKEN_EOF);

  char c = advance();
 
	if (c >= '0' && c <= '9') {
    while (peek() >= '0' && peek() <= '9') advance();
    return make_token(TOKEN_INT);
  }

  switch (c) {
    case '+': return make_token(TOKEN_PLUS);
		case '-': return make_token(TOKEN_MINUS);
		case '*': return make_token(TOKEN_STAR);
		case '/': return make_token(TOKEN_SLASH);
  }
	
	return make_token(TOKEN_ERROR);
  
	// exit(1);
}

// testing here
/*
int main(int argc, char** argv) {

  init_scanner(test_str);

	while (1) {
	  Token token = scan_token();

	  printf("token type: %d\n", token.type);
		printf("token: \"%.*s\"\n", token.length, token.start);

		if (token.type == TOKEN_EOF) break;
  }

  return 0;
}
*/

