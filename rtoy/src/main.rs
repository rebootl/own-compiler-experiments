use std::io;
use std::io::Write;

#[derive(Debug)]
enum TokenType {
    PLUS,
    MINUS,
    SLASH,
    STAR,
    LITERAL,
    EOF,
    ERROR,
}

#[derive(Debug)]
struct Token {
    token_type: TokenType,
    start: usize,
    end: usize,
}

struct Scanner<'a> {
    source: &'a str,
    current_start: usize,
    current_end: usize,
}

impl<'a> Scanner<'a> {
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

    fn get_current_value(&self) -> &str {
        &self.source[self.current_start..self.current_end]
    }

    fn get_token_value(&self, token: &Token) -> &str {
        &self.source[token.start..token.end]
    }
}

fn main() {
    print!("> ");
    io::stdout().flush().unwrap(); // needed to print without newline

    let mut source = String::new();

    io::stdin()
        .read_line(&mut source)
        .expect("Failed to read line");

    println!("You entered: {source}");

    let mut scanner = Scanner::init(&source);

    let token = scanner.scan_token();
    println!("{:?}", token);
    let token2 = scanner.scan_token();
    println!("{:?}", token2);

    println!("{}", scanner.get_current_value());
    println!("{}", scanner.get_token_value(&token));
}
