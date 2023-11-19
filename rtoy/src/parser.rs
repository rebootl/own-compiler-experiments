// use crate::scanner::Scanner;
use crate::scanner::Token;
use crate::scanner::TokenType;

#[derive(Debug)]
pub enum Element {
    INT(usize),
    // FLOAT(f64),
    // STRING(String),
}

#[derive(Debug)]
pub enum Instruction {
    ADD,
    SUB,
    MUL,
    DIV,
    NEG,
    LIT(usize),
}

pub struct ParserResult {
    pub instructions: Vec<Instruction>,
    pub literals: Vec<Element>,
    pub had_error: bool,
    pub error_message: String,
}

pub struct Parser<'a> {
    current_token_idx: usize,
    source: &'a str,
    tokens: Vec<Token>,
    result: ParserResult,
}

impl<'a> Parser<'a> {
    pub fn parse(tokens: Vec<Token>, source: &str) -> ParserResult {
        let mut parser = Parser {
            current_token_idx: 0,
            source,
            tokens,
            result: ParserResult {
                instructions: Vec::new(),
                literals: Vec::new(),
                had_error: false,
                error_message: String::new(),
            },
        };
        parser.parse_expression(0);
        parser.result
    }

    fn error(&mut self, message: &str) {
        if self.result.had_error {
            return;
        }
        self.result.had_error = true;
        self.result.error_message = message.to_string();
    }

    fn consume(&mut self, token_type: TokenType) {
        if self.get_current_token().token_type == token_type {
            self.current_token_idx += 1;
            return;
        }
        self.error("Error: Expected token not found");
    }

    fn get_current_token(&self) -> &Token {
        &self.tokens[self.current_token_idx]
    }

    fn get_previous_token(&self) -> &Token {
        &self.tokens[self.current_token_idx - 1]
    }

    fn get_precedence(&self, token: &Token) -> i8 {
        match token.token_type {
            TokenType::PLUS | TokenType::MINUS => 50,
            TokenType::STAR | TokenType::SLASH => 60,
            _ => -1,
        }
    }

    fn get_token_value(&self, token: &Token) -> usize {
        self.source[token.start..token.end]
            .parse::<usize>()
            .expect("Failed to parse token value")
    }

    fn prefix_handler(&mut self) {
        let token = self.get_previous_token();
        match token.token_type {
            TokenType::LITERAL => {
                let literal = self.get_token_value(token);

                self.result.literals.push(Element::INT(literal));
                self.result
                    .instructions
                    .push(Instruction::LIT(self.result.literals.len() - 1));
            }
            TokenType::MINUS => {
                self.parse_expression(70);
                self.result.instructions.push(Instruction::NEG);
            }
            TokenType::LEFT_PAREN => {
                self.parse_expression(0);
                self.consume(TokenType::RIGHT_PAREN);
            }
            _ => {
                self.error("Error: Unexpected token");
            }
        }
    }

    fn infix_handler(&mut self) {
        let token = self.get_previous_token().clone();

        self.parse_expression(self.get_precedence(&token));

        match token.token_type {
            TokenType::PLUS => {
                self.result.instructions.push(Instruction::ADD);
            }
            TokenType::MINUS => {
                self.result.instructions.push(Instruction::SUB);
            }
            TokenType::STAR => {
                self.result.instructions.push(Instruction::MUL);
            }
            TokenType::SLASH => {
                self.result.instructions.push(Instruction::DIV);
            }
            _ => {
                self.error("Error: Unexpected token");
            }
        }
    }

    fn parse_expression(&mut self, rbp: i8) {
        self.current_token_idx += 1;
        self.prefix_handler();

        loop {
            if rbp > self.get_precedence(&self.get_current_token()) {
                return;
            }
            self.current_token_idx += 1;

            self.infix_handler();
        }
    }
}
