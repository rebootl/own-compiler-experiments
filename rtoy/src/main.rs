use std::io;
use std::io::Write;

mod element;

mod scanner;
use scanner::Scanner;

mod parser;
use parser::Parser;
use parser::ParserResult;

mod interpreter;
use interpreter::Interpreter;
use interpreter::InterpreterResult;

fn main() {
    loop {
        print!("> ");
        io::stdout().flush().unwrap(); // needed to print without newline

        let mut source = String::new();

        io::stdin()
            .read_line(&mut source)
            .expect("Failed to read line");

        // println!("You entered: {source}");

        let tokens: Vec<scanner::Token> = Scanner::scan(&source);
        // println!("{:?}", tokens);
        /*println!("Tokens:");
        for token in &tokens {
            println!("{:?}", token.token_type);
        }*/

        if tokens.len() == 1 {
            continue;
        }
        let parser_result: ParserResult = Parser::parse(tokens, &source);

        if parser_result.had_error {
            println!("{}", parser_result.error_message);
            continue;
        }

        println!("Instructions:");
        println!("  {:?}", parser_result.instructions);
        println!("Literals:");
        println!("  {:?}", parser_result.literals);

        let interpreter_result: InterpreterResult =
            Interpreter::interpret(parser_result.instructions, parser_result.literals);

        if interpreter_result.had_error {
            println!("{}", interpreter_result.error_message);
            continue;
        }

        println!("Result:");
        println!("  {:?}", interpreter_result.value);
    }
}
