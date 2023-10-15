#!/bin/bash

if [ $# -ne 1 ]; then
    echo "Usage: $0 <program name>"
    exit 1
fi

./compiler.py "$1"

nasm -f elf32 -g out.asm -o out.o
#ld -m elf_i386 -o out out.o
gcc -no-pie -m32 -g -o out out.o extends/extensions.o
./out

#echo -e "Exit code: $?"
