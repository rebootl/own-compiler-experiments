#ifndef CONCAT_H
#define CONCAT_H

void print_i(int n);
void println_i(int n);
void print(char *s);
void println();

char *allocate_str(char *s);
void free_str(char *s);

char *int_to_str(int n);

char *concat(char *s1, char *s2);
char *substr(char *s, int start, int end);
int len(char *s);

#endif
