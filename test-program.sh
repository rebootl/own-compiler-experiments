#!/bin/bash

./compiler.py > program.asm

nasm -f elf32 program.asm -o program.o
ld -m elf_i386 -o program program.o
./program
echo $?
