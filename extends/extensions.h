#ifndef EXTENSIONS_H
#define EXTENSIONS_H

// Types

typedef enum {
  NIL,
  BOOL,
  INT,
  STRING,
  ARRAY,
  FUNCTION
} Type;

typedef enum {
  FALSE,
  TRUE
} Bool;

typedef struct Array Array;
typedef struct Element Element;

typedef union {
  int value;
  char *string;
  Array *array;
  // function pointer w/ variable arguments
  Element (*function)(Element, ...);
} UType;

typedef struct Element {
  Type type;
  UType el;
  //char *(*str)(UType);
} Element;

typedef struct Array {
  int size;
  int capacity;
  Element *elements;
} Array;

// Elements

Element *new_Nil();
Element *new_Bool(Bool b);
Element *new_Int(int n);
Element *new_String(char* s);
Element *new_Array(int size);
Element *new_Function(Element (*f)(Element n, ...));

// void print_i(int n);
char *str(Element *e);
void print(Element *e);

// Manipulate
void append(Element *e1, Element *e2);

// void print_i(int n);
//void println_i(int n);
// void print(char *s);
//void println();

/*
typedef struct {
  int size;
  int capacity;
  char *data;
} String;

String *String_new(char *s);
String *Int2str(int n);
String *Substr(String *s, int begin, int end);
String *Concat(String *s1, char *s2);
*/

// Create
// char *String(char *s);
char *Int2str(int n);
char *Concat(char *s1, char *s2);
char *Substr(char *s, int begin, int end);
char *Revstr(char *s);
char *Upper(char *s, int begin, int end);
char *Lower(char *s, int begin, int end);
// todo:
//char *Insert(char *s, char *s1, int i);
//char *Remove(char *s, int begin, int end);
//char *ReplaceAll(char *s, char *s1, char *s2);
//char *Replace(char *s, char *s1, char *s2);
//char *Trim(char *s, char *s1);
//char *TrimLeft(char *s, char *s1);
//char *TrimRight(char *s, char *s1);

// Destroy
void free_str(char *s);


// Query
int len(char *s);
// todo:
//int index_of(char *s, char *s1);
//int equals(char *s, char *s1);
//int starts_with(char *s, char *s1);
//int ends_with(char *s, char *s1);
//int contains(char *s, char *s1);


int addr(void *p);
char *addr2str(int n);

// typedef struct {
//   int size;
//   int capacity;
//   int *data;
//   int *types;
// } Array;

// Create
Array *Array_new(int size);
Array *Copy(Array *a); // shallow copy
Array *Slice(int begin, int end, Array *a);

// Destroy
void  free_array(Array *a);

// Manipulate
// -> arguments reversed because we will push from right to left in compiler
void  put(int i, Type t, int n, Array *a);
void  push(Type t, int n, Array *a);
int   pop(Array *a);
// -> not really nessesary
//int   shift(Array *a);
//int   unshift(Array *a, int n, Type t);
void  insert(int i, Type t, int n, Array *a);
void  remove_at(int i, Array *a);
void  reverse(Array *a);
void  sort(Array *a);

// Query
int   get(int i, Array *a);
char  *get_type(int i, Array *a);
int   size(Array *a);
void  print_array(Array *a);
// -> todo:
//int   index_of_int(Array *a, int n);
//int   index_of_str(Array *a, char *s);
char *stringify(Array *a);


#endif
