#ifndef scanner_h
#define scanner_h

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

void initScanner(const char* source);

Token scanToken();

#endif /* scanner_h */

