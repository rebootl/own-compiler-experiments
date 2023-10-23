#!/bin/bash
#

# extensions library
gcc -m32 -g -c extensions.c -o extensions.o

# testing
gcc -m32 -g -c extensions-test.c -o extensions-test.o
gcc -m32 -g extensions-test.o extensions.o -o extensions-test
./extensions-test

#echo -e "Exit code: $?"
