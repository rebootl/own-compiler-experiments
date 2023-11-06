#ifndef EXTENSIONS_H
#define EXTENSIONS_H

void *_alloc(int size);
void *_realloc(void *p, int size);

// Types

typedef enum {
  NIL,
  BOOL,
  INT,
  FLOAT,
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
  float fvalue;
  char *string;
  Array *array;
  Element (*function)(Element, ...); // function pointer w/ variable arguments
} UType;

/*typedef Element *(*TypeOperation)(Element *e1, Element *e2);

typedef enum {
  ADD,
  SUB,
  MUL,
  DIV,
} Ops;

TypeOperation type_operation[][] = {
  // NIL     BOOL    INT     FLOAT   STRING  ARRAY   FUNCTION
  {NULL,    NULL,   addi,   addf,   NULL,   NULL,   NULL},  // ADD
  {NULL,    NULL,   subi,   subf,   NULL,   NULL,   NULL},  // SUB
  {NULL,    NULL,   muli,   mulf,   NULL,   NULL,   NULL},  // MUL
  {NULL,    NULL,   divi,   divf,   NULL,   NULL,   NULL},  // DIV
};*/

typedef struct Element {
  Type type;
  UType el;
} Element;

typedef struct Array {
  int size;
  int capacity;
  Element *elements;
} Array;

// Create

Element *new_Nil();
Element *new_Bool(Bool b);
Element *new_Int(int n);
Element *new_Float(float f);
Element *new_String(char* s);
Element *new_Array(int size);
Element *new_Function(Element (*f)(Element n, ...));

// Stringify, Print
char *str(Element *e);
void print(Element *e);

// Destroy
void destroy(Element *e);

// Manipulate
int append(Element *e1, Element *e2);
void set(int i, Element *e1, Element *e2);

Element *pop(Element *e);

Element *remove_at(int i, Element *e);
void insert_at(int i, Element *e1, Element *e2);

// Convert
Element *to_bool(Element *e);
Element *to_int(Element *e);
Element *to_float(Element *e);
Element *to_string(Element *e);

// Query
Element *is_nil(Element *e);
Element *is_bool(Element *e);
Element *is_int(Element *e);
Element *is_float(Element *e);
Element *is_string(Element *e);
Element *is_array(Element *e);
Element *is_function(Element *e);

Element *get_type(Element *e);
Element *len(Element *e);

Element *get(int i, Element *e);

// Math
Element *add(Element *e1, Element *e2);
Element *sub(Element *e1, Element *e2);
Element *mul(Element *e1, Element *e2);
Element *_div(Element *e1, Element *e2);
Element *mod(Element *e1, Element *e2);
Element *_pow(Element *e1, Element *e2);
Element *neg(Element *e);

// Compare
Element *eq(Element *e1, Element *e2);
Element *ne(Element *e1, Element *e2);
Element *lt(Element *e1, Element *e2);
Element *le(Element *e1, Element *e2);
Element *gt(Element *e1, Element *e2);
Element *ge(Element *e1, Element *e2);

// Logic
Element *_and(Element *e1, Element *e2);
Element *_or(Element *e1, Element *e2);
Element *_not(Element *e);

// Array
// Element *get(int i, Element *e);
// void put(int i, Element *e1, Element *e2);
// void push(Element *e1, Element *e2);
// Element *pop(Element *e);

// String *Substr(String *s, int begin, int end);
// String *Concat(String *s1, char *s2);

// Create
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



// Query
// todo:
//int index_of(char *s, char *s1);
//int starts_with(char *s, char *s1);
//int ends_with(char *s, char *s1);
//int contains(char *s, char *s1);

// int addr(void *p);
// char *addr2str(int n);

// Create
// Array *Array_new(int size);
Array *Copy(Array *a); // shallow copy
Array *Slice(int begin, int end, Array *a);


// Manipulate
// -> arguments reversed because we will push from right to left in compiler
// void  put(int i, Type t, int n, Array *a);
void  push(Type t, int n, Array *a);
// int   pop(Array *a);
// -> not really nessesary
//int   shift(Array *a);
//int   unshift(Array *a, int n, Type t);
void  insert(int i, Type t, int n, Array *a);
// void  remove_at(int i, Array *a);
void  reverse(Array *a);
void  sort(Array *a);

// Query
// int   get(int i, Array *a);
// char  *get_type(int i, Array *a);
int   size(Array *a);
void  print_array(Array *a);
// -> todo:
//int   index_of_int(Array *a, int n);
//int   index_of_str(Array *a, char *s);

#endif
