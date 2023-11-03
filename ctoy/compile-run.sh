


# compile scanner
gcc -g -c scanner.c -o scanner.o

# interpreter
gcc -g -c interpreter.c -o interpreter.o
gcc -g -c parser.c -o parser.o

gcc -g interpreter.o scanner.o parser.o \
  -o interpreter

# gcc -g -c main.c -o main.o
# ./scanner
./interpreter
