#!/bin/bash
#

if [ $# -ne 1 ]; then
    echo "Usage: $0 <program name>"
    exit 1
fi

#./compiler.py > "$1.asm"

nasm -f elf32 "$1.asm" -o "$1.o"
ld -m elf_i386 -o "$1" "$1.o"
./"$1"
#echo $?
