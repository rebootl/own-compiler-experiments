#ifndef EXTENSIONS_H
#define EXTENSIONS_H

void print_i(int n);
//void println_i(int n);
void print(char *s);
//void println();

char *String(char *s);
void free_str(char *s);

char *Int2str(int n);

char *Concat(char *s1, char *s2);
char *Substr(char *s, int begin, int end);
char *Reverse(char *s);
char *Upper(char *s, int begin, int end);
char *Lower(char *s, int begin, int end);
int len(char *s);

#endif
