#[derive(Debug, PartialEq, Clone)]
#[allow(non_camel_case_types)]
pub enum TokenType {
    Plus,
    Minus,
    Slash,
    Star,
    Literal,
    Right_Paren,
    Left_Paren,
    EOF,
    Error,
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
            tokens.push(token);
            if tokens.last().unwrap().token_type == TokenType::EOF {
                break;
            }
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

        if self.is_at_end() {
            return self.make_token(TokenType::EOF);
        }

        let c = self.advance();

        if Scanner::is_digit(c) {
            while Scanner::is_digit(self.peek()) {
                self.current_end += 1;
            }
            return self.make_token(TokenType::Literal);
        }

        match c {
            '+' => return self.make_token(TokenType::Plus),
            '-' => return self.make_token(TokenType::Minus),
            '*' => return self.make_token(TokenType::Star),
            '/' => return self.make_token(TokenType::Slash),
            '(' => return self.make_token(TokenType::Left_Paren),
            ')' => return self.make_token(TokenType::Right_Paren),
            _ => return self.make_token(TokenType::Error),
        }
    }
}
