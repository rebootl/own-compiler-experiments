use crate::scanner::Scanner;
use crate::scanner::Token;

pub struct Parser {
    current_token: Token,
    previous_token: Option<Token>,
}

impl Parser {
    pub fn init(mut scanner: Scanner) -> Parser {
        let current_token = scanner.scan_token();

        Parser {
            current_token: current_token,
            previous_token: None,
        }
    }
}
