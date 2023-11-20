use crate::element::Element;

use crate::parser::Instruction;

pub struct InterpreterResult {
    pub value: Element,
    pub had_error: bool,
    pub error_message: String,
}

pub struct Interpreter {
    stack: Vec<Element>,
    ptr: usize,
    instructions: Vec<Instruction>,
    literals: Vec<Element>,
    result: InterpreterResult,
}

impl Interpreter {
    pub fn interpret(instructions: Vec<Instruction>, literals: Vec<Element>) -> InterpreterResult {
        let mut interpreter = Interpreter {
            stack: Vec::new(),
            ptr: 0,
            instructions,
            literals,
            result: InterpreterResult {
                value: Element::Nil,
                had_error: false,
                error_message: String::new(),
            },
        };
        interpreter.run();
        interpreter.result.value = interpreter.stack.pop().unwrap();
        interpreter.result
    }
    fn run(&mut self) {
        loop {
            let instruction = &self.instructions[self.ptr];
            match *instruction {
                Instruction::Lit(idx) => {
                    let literal = self.literals[idx].clone();
                    self.stack.push(literal);
                }
                Instruction::Add => {
                    let a = self.stack.pop().unwrap();
                    let b = self.stack.pop().unwrap();
                    let result = a.add(&b);
                    match result {
                        Some(element) => self.stack.push(element),
                        None => {
                            self.result.had_error = true;
                            self.result.error_message = format!(
                                "Add operation not implemented for types {:?} and {:?}",
                                a, b
                            );
                            break;
                        }
                    }
                }
                _ => {}
            }
            self.ptr += 1;
            if self.ptr >= self.instructions.len() {
                break;
            }
        }
    }
}
