#!/bin/bash
#

# extensions library
gcc -m32 -c extensions.c -o extensions.o

# testing
gcc -m32 -c extensions-test.c -o extensions-test.o
gcc -m32 extensions-test.o extensions.o -o extensions-test
./extensions-test

#echo -e "Exit code: $?"
