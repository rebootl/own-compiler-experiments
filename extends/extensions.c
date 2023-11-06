/* c extensions lib */

#include <stdio.h>  // for printf
#include <string.h> // for strlen, strcpy, strcat
#include <stdlib.h> // for malloc

#include "extensions.h"

// Helper forw. decl. (impl. below)

void *_alloc(int size);
void *_realloc(void *p, int size);

int append(Element *e1, Element *e2);
char *str(Element *e);

int _len(Element *e);
int _get_abs_index(int index, Element *e);

// Elements

Element *new_Nil() {
  Element *result = _alloc(sizeof(Element));
  result->type = NIL;
  result->el.value = 0;
  return result;
}

Element *new_Bool(Bool b) {
  Element *result = _alloc(sizeof(Element));
  result->type = BOOL;
  result->el.value = b;
  return result;
}

Element *new_Int(int n) {
  Element *result = _alloc(sizeof(Element));
  result->type = INT;
  result->el.value = n;
  return result;
}

Element *new_Float(float f) {
  Element *result = _alloc(sizeof(Element));
  result->type = FLOAT;
  result->el.fvalue = f;
  return result;
}

Element *new_String(char* s) {
  char *r = _alloc(strlen(s) + 1); //+1 for the zero-terminator
  strcpy(r, s);

  Element *result = _alloc(sizeof(Element));
  result->type = STRING;
  result->el.string = r;
  return result;
}

Element *new_Array(int size) {
  Array *r = _alloc(sizeof(Array));
  r->size = size;
  r->capacity = size == 0 ? 2 : size;
  r->elements = _alloc(size * sizeof(Element));

  for (int i = 0; i < size; i++) {
    r->elements[i] = *new_Nil();
  }

  Element *result = _alloc(sizeof(Element));
  result->type = ARRAY;
  result->el.array = r;
  return result;
}

// Stringify

char *_str_Nil(UType u) {
  return "Nil";
}

char *_str_Bool(UType u) {
  if (u.value) {
    return "True";
  }
  return "False";
}

char *_str_Int(UType u) {
  char *result = _alloc(12); // 12 is the max length of an int

  sprintf(result, "%d", u.value);
  return result;
}

char *_str_Float(UType u) {
  // assuming 32 bit float
  // -> improve this ?
  char *result = _alloc(12);

  sprintf(result, "%f", u.fvalue);
  return result;
}

char *_str_String(UType u) {
  return u.string;
}

char *_str_Array(UType u) {
  Element *r = new_String("[ ");
  Element *sep = new_String(", ");
  Element *end = new_String(" ]");
  Element *quote = new_String("\"");
  for (int i = 0; i < u.array->size; i++) {
    if (i > 0) {
      append(r, sep);
    }
    if (u.array->elements[i].type == STRING) {
      append(r, quote);
      append(r, new_String(u.array->elements[i].el.string));
      append(r, quote);
    } else {
      Element *arr = new_String(str(&u.array->elements[i]));
      append(r, arr);
      destroy(arr);
    }
  }
  append(r, new_String(" ]"));
  destroy(quote);
  destroy(sep);
  destroy(end);
  return r->el.string;
}

char *str(Element *e) {
  switch (e->type) {
    case NIL:
      return _str_Nil(e->el);
    case BOOL:
      return _str_Bool(e->el);
    case INT:
      return _str_Int(e->el);
    case FLOAT:
      return _str_Float(e->el);
    case STRING:
      return _str_String(e->el);
    case ARRAY:
      return _str_Array(e->el);
    default:
      return "oops todo";
  }
}

// Print

void print(Element *e) {
  printf("%s", str(e));
  // fflush may be needed, otherwise the output is not printed
  fflush(stdout);
}

// Destroy

void destroy(Element *e) {
  if (e->type == STRING) {
    free(e->el.string);
  } else if (e->type == ARRAY) {
    free(e->el.array->elements);
    free(e->el.array);
  }
  free(e);
}

// Manipulate
void _grow_array(Element *e) {
  e->el.array->capacity *= 2;
  e->el.array->elements = _realloc(e->el.array->elements, e->el.array->capacity * sizeof(Element));
}

void _shrink_array(Element *e) {
  e->el.array->capacity /= 2;
  e->el.array->elements = _realloc(e->el.array->elements, e->el.array->capacity * sizeof(Element));
}

int append(Element *e1, Element *e2) {
  if (e1->type == STRING && e2->type == STRING) {
    char *r = _realloc(e1->el.string, _len(e1) + _len(e2) + 1);
    strcat(r, e2->el.string);
    e1->el.string = r;
    return _len(e1) - 1;
  }
  if (e1->type == ARRAY) {
    if (e1->el.array->size == e1->el.array->capacity) {
      _grow_array(e1);
    }
    e1->el.array->elements[e1->el.array->size] = *e2;
    e1->el.array->size++;
    return _len(e1) - 1;
  }
  printf("append not implemented for type %d\n", e1->type);
  exit(1);
}

void set(int index, Element *e1, Element *e2) {
  int i = _get_abs_index(index, e1);
  if (i >= _len(e1)) {
    printf("index out of bounds\n");
    exit(1);
  }
  if (e1->type == ARRAY) {
    e1->el.array->elements[i] = *e2;
    return;
  }
  if (e1->type == STRING && e2->type == STRING) {
    if (_len(e2) != 1) {
      printf("string to set must be of length 1\n");
      exit(1);
    }
    e1->el.string[i] = e2->el.string[0];
    return;
  }
  printf("set not implemented for type %d\n", e1->type);
  exit(1);
}

Element *pop(Element *e) {
  if (e->type == ARRAY) {
    if (_len(e) == 0) {
      printf("pop from empty array\n");
      exit(1);
    }
    e->el.array->size--;
    Element *result = &e->el.array->elements[e->el.array->size];
    
    // shrink array if size < capacity / 2
    if (e->el.array->size < e->el.array->capacity / 2) {
      _shrink_array(e);
    }
    
    return result;
  }
  printf("pop not implemented for type %d\n", e->type);
  exit(1);
}

Element *remove_at(int index, Element *e) {
  int i = _get_abs_index(index, e);
  if (i >= _len(e)) {
    printf("index out of bounds\n");
    exit(1);
  }
  if (e->type == ARRAY) {
    Element *result = &e->el.array->elements[i];
    for (int j = i; j < _len(e) - 1; j++) {
      e->el.array->elements[j] = e->el.array->elements[j + 1];
    }
    e->el.array->size--;

    // shrink array if size < capacity / 2
    if (e->el.array->size < e->el.array->capacity / 2) {
      _shrink_array(e);
    }
    return result;
  }
  printf("remove not implemented for type %d\n", e->type);
  exit(1);
}

void insert_at(int index, Element *e1, Element *e2) {
  int i = _get_abs_index(index, e1);
  if (i > _len(e1)) {
    printf("index out of bounds\n");
    exit(1);
  }
  if (e1->type == ARRAY) {
    if (e1->el.array->size == e1->el.array->capacity) {
      _grow_array(e1);
    }
    for (int j = _len(e1) - 1; j >= i; j--) {
      e1->el.array->elements[j + 1] = e1->el.array->elements[j];
    }
    e1->el.array->elements[i] = *e2;
    e1->el.array->size++;
  }
  printf("insert not implemented for type %d\n", e1->type);
  exit(1);
}

// Convert

Element *to_Bool(Element *e) {
  switch (e->type) {
    case NIL:
      return new_Bool(FALSE);
    case BOOL:
      return e;
    case INT:
      return new_Bool(e->el.value != 0);
    case FLOAT:
      return new_Bool(e->el.fvalue != 0.0);
    default:
      printf("to_bool not implemented for type %d\n", e->type);
      exit(1);
  }
}

Element *to_Int(Element *e) {
  switch (e->type) {
    case NIL:
      return new_Int(0);
    case BOOL:
      return new_Int(e->el.value);
    case INT:
      return e;
    case FLOAT:
      return new_Int((int)e->el.fvalue);
    default:
      printf("to_int not implemented for type %d\n", e->type);
      exit(1);
  }
}

Element *to_Float(Element *e) {
  switch (e->type) {
    case NIL:
      return new_Float(0.0);
    case BOOL:
      return new_Float(e->el.value);
    case INT:
      return new_Float(e->el.value);
    case FLOAT:
      return e;
    default:
      printf("to_float not implemented for type %d\n", e->type);
      exit(1);
  }
}

Element *to_String(Element *e) {
  switch (e->type) {
    case NIL:
      return new_String("Nil");
    case BOOL:
      if (e->el.value) {
        return new_String("True");
      } else {
        return new_String("False");
      }
    case INT:
      return new_String(_str_Int(e->el));
    case FLOAT:
      return new_String(_str_Float(e->el));
    case STRING:
      return e;
    default:
      printf("to_string not implemented for type %d\n", e->type);
      exit(1);
  }
}

// Query

Element *is_Nil(Element *e) {
  if (e->type == NIL) {
    return new_Bool(TRUE);
  }
  return new_Bool(FALSE);
}

Element *is_Bool(Element *e) {
  if (e->type == BOOL) {
    return new_Bool(TRUE);
  }
  return new_Bool(FALSE);
}

Element *is_Int(Element *e) {
  if (e->type == INT) {
    return new_Bool(TRUE);
  }
  return new_Bool(FALSE);
}

Element *is_Float(Element *e) {
  if (e->type == FLOAT) {
    return new_Bool(TRUE);
  }
  return new_Bool(FALSE);
}

Element *is_String(Element *e) {
  if (e->type == STRING) {
    return new_Bool(TRUE);
  }
  return new_Bool(FALSE);
}

Element *is_Array(Element *e) {
  if (e->type == ARRAY) {
    return new_Bool(TRUE);
  }
  return new_Bool(FALSE);
}

Element *is_Function(Element *e) {
  if (e->type == FUNCTION) {
    return new_Bool(TRUE);
  }
  return new_Bool(FALSE);
}

Element *get_type(Element *e) {
  switch (e->type) {
    case NIL:
      return new_String("Nil");
    case BOOL:
      return new_String("Bool");
    case INT:
      return new_String("Int");
    case FLOAT:
      return new_String("Float");
    case STRING:
      return new_String("String");
    case ARRAY:
      return new_String("Array");
    case FUNCTION:
      return new_String("Function");
    default:
      printf("get_type not implemented for type %d\n", e->type);
      exit(1);
  }
}

Element *len(Element *e) {
  if (e->type == STRING) {
    return new_Int(strlen(e->el.string));
  }
  if (e->type == ARRAY) {
    return new_Int(e->el.array->size);
  }
  printf("len only works on String and Array\n");
  exit(1);
}

Element *get(int index, Element *e) {
  int i = _get_abs_index(index, e);
  if (i >= _len(e)) {
    printf("index out of bounds\n");
    exit(1);
  }
  if (e->type == STRING) {
    return new_String(Substr(e->el.string, i, i));
  }
  if (e->type == ARRAY) {
    return &e->el.array->elements[i];
  }
  printf("get not implemented for type %d\n", e->type);
  exit(1);
}

// Math

Element *add(Element *e1, Element *e2) {
  if (e1->type == INT && e2->type == INT) {
    return new_Int(e1->el.value + e2->el.value);
  }
  if (e1->type == FLOAT && e2->type == FLOAT) {
    return new_Float(e1->el.fvalue + e2->el.fvalue);
  }
  printf("add only works on Int + Int and Float + Float\n");
  exit(1);
}

Element *sub(Element *e1, Element *e2) {
  if (e1->type == INT && e2->type == INT) {
    return new_Int(e1->el.value - e2->el.value);
  }
  if (e1->type == FLOAT && e2->type == FLOAT) {
    return new_Float(e1->el.fvalue - e2->el.fvalue);
  }
  printf("sub only works on Int - Int and Float - Float\n");
  exit(1);
}

Element *mul(Element *e1, Element *e2) {
  if (e1->type == INT && e2->type == INT) {
    return new_Int(e1->el.value * e2->el.value);
  }
  if (e1->type == FLOAT && e2->type == FLOAT) {
    return new_Float(e1->el.fvalue * e2->el.fvalue);
  }
  printf("mul only works on Int * Int and Float * Float\n");
  exit(1);
}

Element *_div(Element *e1, Element *e2) {
  if (e1->type == INT && e2->type == INT) {
    if (e2->el.value == 0) {
      printf("division by zero\n");
      exit(1);
    }
    return new_Int(e1->el.value / e2->el.value);
  }
  if (e1->type == FLOAT && e2->type == FLOAT) {
    if (e2->el.fvalue == 0) {
      printf("division by zero\n");
      exit(1);
    }
    return new_Float(e1->el.fvalue / e2->el.fvalue);
  }
  printf("div only works on Int / Int and Float / Float\n");
  exit(1);
}

Element *mod(Element *e1, Element *e2) {
  if (e1->type != INT || e2->type != INT) {
    printf("mod only works on ints\n");
    exit(1);
  }
  // todo: -> float mod ? => use fmod from math.h
  return new_Int(e1->el.value % e2->el.value);
}

Element *_pow(Element *e1, Element *e2) {
  if (e1->type != INT || e2->type != INT) {
    printf("pow only works on ints\n");
    exit(1);
  }
  // todo: -> float pow ? => use pow from math.h
  return new_Int(e1->el.value ^ e2->el.value);
}

Element *neg(Element *e) {
  if (e->type == INT) {
    return new_Int(-e->el.value);
  }
  if (e->type == FLOAT) {
    return new_Float(-e->el.fvalue);
  }
  printf("neg only works on Int and Float\n");
  exit(1);
}

// Compare

Element *eq(Element *e1, Element *e2) {
  if (e1->type == INT && e2->type == INT) {
    return new_Bool(e1->el.value == e2->el.value);
  }
  if (e1->type == FLOAT && e2->type == FLOAT) {
    return new_Bool(e1->el.fvalue == e2->el.fvalue);
  }
  if (e1->type == STRING && e2->type == STRING) {
    return new_Bool(strcmp(e1->el.string, e2->el.string) == 0);
  }
  printf("eq only works on Int == Int, Float == Float and String == String\n");
  exit(1);
}

Element *ne(Element *e1, Element *e2) {
  if (e1->type == INT && e2->type == INT) {
    return new_Bool(e1->el.value != e2->el.value);
  }
  if (e1->type == FLOAT && e2->type == FLOAT) {
    return new_Bool(e1->el.fvalue != e2->el.fvalue);
  }
  if (e1->type == STRING && e2->type == STRING) {
    return new_Bool(strcmp(e1->el.string, e2->el.string) != 0);
  }
  printf("ne only works on Int != Int, Float != Float and String != String\n");
  exit(1);
}

Element *lt(Element *e1, Element *e2) {
  if (e1->type == INT && e2->type == INT) {
    return new_Bool(e1->el.value < e2->el.value);
  }
  if (e1->type == FLOAT && e2->type == FLOAT) {
    return new_Bool(e1->el.fvalue < e2->el.fvalue);
  }
  if (e1->type == STRING && e2->type == STRING) {
    return new_Bool(strcmp(e1->el.string, e2->el.string) < 0);
  }
  printf("lt only works on Int < Int, Float < Float and String < String\n");
  exit(1);
}

Element *le(Element *e1, Element *e2) {
  if (e1->type == INT && e2->type == INT) {
    return new_Bool(e1->el.value <= e2->el.value);
  }
  if (e1->type == FLOAT && e2->type == FLOAT) {
    return new_Bool(e1->el.fvalue <= e2->el.fvalue);
  }
  if (e1->type == STRING && e2->type == STRING) {
    return new_Bool(strcmp(e1->el.string, e2->el.string) <= 0);
  }
  printf("le only works on Int <= Int, Float <= Float and String <= String\n");
  exit(1);
}

Element *gt(Element *e1, Element *e2) {
  if (e1->type == INT && e2->type == INT) {
    return new_Bool(e1->el.value > e2->el.value);
  }
  if (e1->type == FLOAT && e2->type == FLOAT) {
    return new_Bool(e1->el.fvalue > e2->el.fvalue);
  }
  if (e1->type == STRING && e2->type == STRING) {
    return new_Bool(strcmp(e1->el.string, e2->el.string) > 0);
  }
  printf("gt only works on Int > Int, Float > Float and String > String\n");
  exit(1);
}

Element *ge(Element *e1, Element *e2) {
  if (e1->type == INT && e2->type == INT) {
    return new_Bool(e1->el.value >= e2->el.value);
  }
  if (e1->type == FLOAT && e2->type == FLOAT) {
    return new_Bool(e1->el.fvalue >= e2->el.fvalue);
  }
  if (e1->type == STRING && e2->type == STRING) {
    return new_Bool(strcmp(e1->el.string, e2->el.string) >= 0);
  }
  printf("ge only works on Int >= Int, Float >= Float and String >= String\n");
  exit(1);
}

// Logic

Element *_and(Element *e1, Element *e2) {
  if (e1->type != BOOL || e2->type != BOOL) {
    printf("and only works on Bool and Bool\n");
    exit(1);
  }
  return new_Bool(e1->el.value && e2->el.value);
}

Element *_or(Element *e1, Element *e2) {
  if (e1->type != BOOL || e2->type != BOOL) {
    printf("or only works on Bool and Bool\n");
    exit(1);
  }
  return new_Bool(e1->el.value || e2->el.value);
}

Element *_not(Element *e) {
  if (e->type != BOOL) {
    printf("not only works on Bool\n");
    exit(1);
  }
  return new_Bool(!e->el.value);
}



// Helper impl.

void *_alloc(int size) {
  void *result = malloc(size);
  if (result == NULL) {
      printf("malloc failed\n");
      exit(1);
  }
  return result;
}

void *_realloc(void *p, int size) {
  void *result = realloc(p, size);
  if (result == NULL) {
      printf("realloc failed\n");
      exit(1);
  }
  return result;
}

int _len(Element *e) {
  return len(e)->el.value;
}

int _get_abs_index(int index, Element *e) {
  int l = _len(e);
  if (index < 0) {
    return l + index;
  }
  return index;
}


/* concat, string concatenation

  s1: memory address of first string
  s2: memory address of second string

  - allocates memory for the concatenated string
  - writes the concatenated string to the allocated memory

  returns: memory address of concatenated string

*/
char *Concat(char *s1, char *s2) {
  char *result = _alloc(strlen(s1) + strlen(s2) + 1); //+1 for the zero-terminator

  strcpy(result, s1);
  strcat(result, s2);
  return result;
}

int _get_start_index(int start, int len) {
  if (start < 0) {
    return len + start;
  }
  if (start > len) {
    return len;
  }
  return start;
}

int _get_stop_index(int stop, int len) {
  if (stop < 0) {
    return len + stop;
  }
  if (stop > len) {
    return len - 1;
  }
  return stop;
}

char *Substr(char *s, int begin, int end) {
  /*if (begin < 0) {
    printf("invalid start or end index\n");
    exit(1);
  }*/
  int start = _get_start_index(begin, strlen(s));
  int stop = _get_stop_index(end, strlen(s));

  char *result = _alloc(stop - start + 2); //+1 for the zero-terminator

  strncpy(result, s + start, stop - start + 1);
  result[stop - start + 1] = '\0';
  return result;
}

char *Revstr(char *s) {
  char *result = _alloc(strlen(s) + 1); //+1 for the zero-terminator

  int i;
  for (i = 0; i < strlen(s); i++) {
    result[i] = s[strlen(s) - i - 1];
  }
  result[strlen(s)] = '\0';
  return result;
}

char *_case(char *s, int begin, int end, int upper) {
  int start = _get_start_index(begin, strlen(s));
  int stop = _get_stop_index(end, strlen(s));

  char *result = _alloc(strlen(s) + 1); //+1 for the zero-terminator

  strcpy(result, s);
  for (int i = start; i <= stop; i++) {
    if (upper) {
      if (s[i] >= 'a' && s[i] <= 'z') {
        result[i] = s[i] - 32;
      } else {
        result[i] = s[i];
      }
    } else {
      if (s[i] >= 'A' && s[i] <= 'Z') {
        result[i] = s[i] + 32;
      } else {
        result[i] = s[i];
      }
    }
  }
  result[strlen(s)] = '\0';
  return result;
}

char *Upper(char *s, int begin, int end) {
  return _case(s, begin, end, 1);
}

char *Lower(char *s, int begin, int end) {
  return _case(s, begin, end, 0);
}
/*
char *Trim(char *s) {
  int start = 0;
  int stop = strlen(s) - 1;

  while (s[start] == ' ' || s[start] == '\t' || s[start] == '\n') {
    start++;
  }
  while (s[stop] == ' ' || s[stop] == '\t' || s[stop] == '\n') {
    stop--;
  }

  char *result = _alloc(stop - start + 2); //+1 for the zero-terminator

  strncpy(result, s + start, stop - start + 1);
  result[stop - start + 1] = '\0';
  return result;
}
*/
/*
char *append(char *s, char *s2) {
  char *r = (char *)_realloc(s, strlen(s) + strlen(s2) + 1);

  //strcpy(r, s);
  strcat(r, s2);
  return r;
}
*/
/*int len(char *s) {
  return strlen(s);
}*/
/*
int addr(void *p) {
  return (int)p;
}

char *addr2str(int n) {
  return (char *)n;
}
*/
/*Array *Array_new(int size) {
  Array *result = _alloc(sizeof(Array));

  result->size = size;
  result->capacity = size;
  result->data = _alloc(result->capacity * sizeof(int));
  result->types = _alloc(result->capacity * sizeof(type));
  return result;
}

void put(int i, type t, int n, Array *a) {
  if (i < 0 || i >= a->size) {
    printf("index out of bounds\n");
    exit(1);
  }
  a->data[i] = n;
  a->types[i] = t;
}

int get(int i, Array *a) {
  if (i < 0 || i >= a->size) {
    printf("index out of bounds\n");
    exit(1);
  }
  return a->data[i];
}

char *get_type(int i, Array *a) {
  if (i < 0 || i >= a->size) {
    printf("index out of bounds\n");
    exit(1);
  }
  switch (a->types[i]) {
    case INT:
      return "INT";
    case STRING:
      return "STRING";
    case ARRAY:
      return "ARRAY";
    default:
      return "UNDEFINED";
  }
}

void _array_grow(Array *a) {
  a->capacity *= 2;
  a->data = _realloc(a->data, a->capacity * sizeof(int));
  a->types = _realloc(a->types, a->capacity * sizeof(type));
}

void _array_shrink(Array *a) {
  a->capacity /= 2;
  a->data = _realloc(a->data, a->capacity * sizeof(int));
  a->types = _realloc(a->types, a->capacity * sizeof(type));
}

void push(type t, int n, Array *a) {
  if (a->size == a->capacity) {
    _array_grow(a);
  }
  a->data[a->size] = n;
  a->types[a->size] = t;
  a->size++;
}

int pop(Array *a) {
  if (a->size == 0) {
    printf("pop from empty array\n");
    exit(1);
  }
  int result = a->data[a->size - 1];
  a->size--;
  if (a->size < a->capacity / 4) {
    a->capacity /= 2;
    a->data = _realloc(a->data, a->capacity * sizeof(int));
    a->types = _realloc(a->types, a->capacity * sizeof(type));
  }
  return result;
}

int size(Array *a) {
  return a->size;
}

void free_array(Array *a) {
  for (int i = 0; i < a->size; i++) {
    if (a->types[i] == STRING) {
      free_str(addr2str(a->data[i]));
    } else if (a->types[i] == ARRAY) {
      free_array((Array *)a->data[i]);
    }
  }
  free(a->data);
  free(a->types);
  free(a);
}

void _print_array(Array *a) {
  printf("[ ");
  for (int i = 0; i < a->size; i++) {
    if (i > 0) {
      printf(", ");
    }
    switch (a->types[i]) {
      case INT:
        printf("%d", a->data[i]);
        break;
      case STRING:
        printf("\"%s\"", addr2str(a->data[i]));
        break;
      case ARRAY:
        _print_array((Array *)a->data[i]);
        break;
      default:
        printf("undefined");
    }
  }
  printf(" ]");
  fflush(stdout);
}

void print_array(Array *a) {
  _print_array(a);
  printf("\n");
  fflush(stdout);
}

char *stringify(Array *a) {
  char *r = String("[ ");
  for (int i = 0; i < a->size; i++) {
    if (i > 0) {
      r = append(r, ", ");
    }
    switch (a->types[i]) {
      case INT:
        r = append(r, Int2str(a->data[i]));
        break;
      case STRING:
        r = append(r, "\"");
        r = append(r, addr2str(a->data[i]));
        r = append(r, "\"");
        break;
      case ARRAY:
        r = append(r, stringify((Array *)a->data[i]));
        break;
      default:
        r = append(r, "undefined");
    }
  }
  r = append(r, " ]");
  return r;
}
/*
int shift(Array *a) {
  if (a->size == 0) {
    printf("shift from empty array\n");
    exit(1);
  }
  int result = a->data[0];
  for (int i = 0; i < a->size - 1; i++) {
    a->data[i] = a->data[i + 1];
    a->types[i] = a->types[i + 1];
  }
  a->size--;
  if (a->size < a->capacity / 4) {
    _array_shrink(a);
  }
  return result;
}

int unshift(int n, type t, Array *a) {
  if (a->size == a->capacity) {
    _array_grow(a);
  }
  for (int i = a->size; i > 0; i--) {
    a->data[i] = a->data[i - 1];
    a->types[i] = a->types[i - 1];
  }
  a->data[0] = n;
  a->types[0] = t;
  a->size++;
  return a->size;
}
*/
/*void insert(int i, type t, int n, Array *a) {
  if (i < 0 || i >= a->size) {
    printf("index out of bounds\n");
    exit(1);
  }
  if (a->size == a->capacity) {
    _array_grow(a);
  }
  for (int j = a->size; j > i; j--) {
    a->data[j] = a->data[j - 1];
    a->types[j] = a->types[j - 1];
  }
  a->data[i] = n;
  a->types[i] = t;
  a->size++;
}

void remove_at(int i, Array *a) {
  if (i < 0 || i >= a->size) {
    printf("index out of bounds\n");
    exit(1);
  }
  for (int j = i; j < a->size - 1; j++) {
    a->data[j] = a->data[j + 1];
    a->types[j] = a->types[j + 1];
  }
  a->size--;
  if (a->size < a->capacity / 4) {
    _array_shrink(a);
  }
}

void reverse(Array *a) {
  for (int i = 0; i < a->size / 2; i++) {
    int tmp = a->data[i];
    type tmp2 = a->types[i];
    a->data[i] = a->data[a->size - i - 1];
    a->types[i] = a->types[a->size - i - 1];
    a->data[a->size - i - 1] = tmp;
    a->types[a->size - i - 1] = tmp2;
  }
}

void _sort_int(Array *a) {
  for (int i = 0; i < a->size; i++) {
    if (a->types[i] != INT) {
      printf("sort does not work on arrays of mixed types\n");
      exit(1);
    }
    for (int j = i + 1; j < a->size; j++) {
      if (a->data[i] > a->data[j]) {
        int tmp = a->data[i];
        a->data[i] = a->data[j];
        a->data[j] = tmp;
      }
    }
  }
}

void _sort_string(Array *a) {
  for (int i = 0; i < a->size; i++) {
    if (a->types[i] != STRING) {
      printf("sort does not work on arrays of mixed types\n");
      exit(1);
    }
    for (int j = i + 1; j < a->size; j++) {
      if (strcmp(addr2str(a->data[i]), addr2str(a->data[j])) > 0) {
        int tmp = a->data[i];
        a->data[i] = a->data[j];
        a->data[j] = tmp;
      }
    }
  }
}

void sort(Array *a) {
  type t = a->types[0];
  switch (t) {
    case INT:
      _sort_int(a);
      break;
    case STRING:
      _sort_string(a);
      break;
    case ARRAY:
      printf("sort does not work on arrays of arrays\n");
      exit(1);
    default:
      printf("sort does not work on arrays of mixed types\n");
      exit(1);
  }
}

Array *Slice(int begin, int end, Array *a) {
  int start = _get_start_index(begin, a->size);
  int stop = _get_stop_index(end, a->size);

  Array *result = Array_new(stop - start + 1);

  for (int i = start; i <= stop; i++) {
    put(i - start, a->types[i], a->data[i], result);
  }
  return result;
}

Array *Copy(Array *a) {
  Array *result = Array_new(a->size);

  for (int i = 0; i < a->size; i++) {
    put(i, a->types[i], a->data[i], result);
  }
  return result;
}
*/
