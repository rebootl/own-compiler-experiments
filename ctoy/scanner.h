#ifndef scanner_h
#define scanner_h

typedef enum {
  TOKEN_INT,
  TOKEN_PLUS,
	TOKEN_MINUS,
	TOKEN_STAR,
	TOKEN_SLASH,
	TOKEN_EOF,
  TOKEN_ERROR,
  TOKEN_LEFT_PAREN,
  TOKEN_RIGHT_PAREN,
  TOKEN_SEMICOLON,
} TokenType;

typedef struct {
  TokenType type;
  const char* start;
  int length;
} Token;

void init_scanner(const char* source);

Token scan_token();

#endif /* scanner_h */

