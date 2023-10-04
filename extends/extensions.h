#ifndef EXTENSIONS_H
#define EXTENSIONS_H

void print_i(int n);
//void println_i(int n);
void print(char *s);
//void println();

char *allocate_str(char *s);
void free_str(char *s);

char *int_to_str(int n);

char *concat(char *s1, char *s2);
char *substr(char *s, int begin, int end);
char *reverse(char *s);
char *uppercase(char *s, int begin, int end);
char *lowercase(char *s, int begin, int end);
int len(char *s);

#endif
