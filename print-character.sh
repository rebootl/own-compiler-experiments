#!/bin/bash

#./compiler.py > program.asm

nasm -f elf32 print-character.asm -o print-character.o
ld -m elf_i386 -o print-character print-character.o
./print-character
#echo $?
