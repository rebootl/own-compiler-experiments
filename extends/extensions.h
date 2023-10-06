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

int addr(void *p);
char *addr2str(int n);

typedef enum {
  INT,
  STRING,
  ARRAY
} type;

typedef struct {
  int size;
  int capacity;
  int *data;
  int *types;
} Array;

Array *Array_new(int capacity);
void  put(Array *a, int i, int n, type t);
int   get(Array *a, int i);
char  *get_type(Array *a, int i);
void  push(Array *a, int n, type t);
int   pop(Array *a);
int   size(Array *a);
void  free_array(Array *a);

void print_array(Array *a);

int shift(Array *a);

#endif
