use std::io;
use std::io::Write;

mod scanner;
use scanner::Scanner;

mod parser;
use parser::Parser;

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
