#!/bin/bash
#

if [ $# -ne 1 ]; then
    echo "Usage: $0 <program name>"
    exit 1
fi

nasm -f elf32 -g "$1" -o out.o
#ld -m elf_i386 -o out out.o
gcc -static -m32 -o out out.o extensions.o
./out

#echo -e "Exit code: $?"
