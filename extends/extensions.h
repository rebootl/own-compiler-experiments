#ifndef CONCAT_H
#define CONCAT_H

void print_i(int n);
void println_i(int n);
void print(char *s);
void println();

char *allocate_str(char *s);
void free_str(char *s);

char *concat(char *s1, char *s2);

#endif
