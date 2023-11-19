#[derive(Debug, PartialEq, Clone)]
pub enum TokenType {
    PLUS,
    MINUS,
    SLASH,
    STAR,
    LITERAL,
    EOF,
    ERROR,
}

#[derive(Debug, Clone)]
pub struct Token {
    pub token_type: TokenType,
    pub start: usize,
    pub end: usize,
}

pub struct Scanner<'a> {
    source: &'a str,
    current_start: usize,
    current_end: usize,
}

impl<'a> Scanner<'a> {
    pub fn scan(source: &str) -> Vec<Token> {
        let mut scanner = Scanner::init(source);
        let mut tokens: Vec<Token> = Vec::new();
        loop {
            let token = scanner.scan_token();
            if token.token_type == TokenType::EOF {
                break;
            }
            tokens.push(token);
        }
        tokens
    }

    fn init(source: &'a str) -> Scanner {
        Scanner {
            source,
            current_start: 0,
            current_end: 0,
        }
    }

    fn is_at_end(&self) -> bool {
        self.current_end >= self.source.len()
    }

    fn advance(&mut self) -> char {
        self.current_end += 1;
        self.source.chars().nth(self.current_end - 1).unwrap()
    }

    fn peek(&self) -> char {
        // checked below already
        // if self.is_at_end() {
        //     return '\0';
        // }
        self.source.chars().nth(self.current_end).unwrap_or('\0')
    }

    fn skip_whitespace(&mut self) {
        loop {
            let c = self.peek();
            match c {
                ' ' | '\r' | '\t' | '\n' => self.current_end += 1,
                _ => break,
            }
        }
        self.current_start = self.current_end;
    }

    fn make_token(&mut self, token_type: TokenType) -> Token {
        Token {
            token_type,
            start: self.current_start,
            end: self.current_end,
        }
    }

    fn is_digit(c: char) -> bool {
        c >= '0' && c <= '9'
    }

    fn scan_token(&mut self) -> Token {
        self.skip_whitespace();
        // self.start = self.end;

        if self.is_at_end() {
            return self.make_token(TokenType::EOF);
        }

        let c = self.advance();

        if Scanner::is_digit(c) {
            while Scanner::is_digit(self.peek()) {
                self.current_end += 1;
            }
            return self.make_token(TokenType::LITERAL);
        }

        match c {
            '+' => return self.make_token(TokenType::PLUS),
            '-' => return self.make_token(TokenType::MINUS),
            '*' => return self.make_token(TokenType::STAR),
            '/' => return self.make_token(TokenType::SLASH),
            _ => return self.make_token(TokenType::ERROR),
        }
    }

    /*
    pub fn get_current_value(&self) -> &str {
        &self.source[self.current_start..self.current_end]
    }

    pub fn get_token_value(&self, token: &Token) -> &str {
        &self.source[token.start..token.end]
    }
    */
    /*
        pub fn get_dummy_token(&self) -> Token {
            Token {
                token_type: TokenType::ERROR,
                start: 0,
                end: 0,
            }
        }
    */
}
