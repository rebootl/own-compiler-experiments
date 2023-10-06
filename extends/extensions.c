/* c extension to concat two strings
*/

#include <stdio.h>  // for printf
#include <string.h> // for strlen, strcpy, strcat
#include <stdlib.h> // for malloc

#include "extensions.h"

/* print functions */

// fflush is needed, otherwise the output is not printed

void print_i(int n) {
  printf("%d", n);
  fflush(stdout);
}

// (not used atm)
/*
void println_i(int n) {
  printf("%d\n", n);
  fflush(stdout);
}
*/
void print(char *s) {
  printf("%s", s);
  fflush(stdout);
}
/*
void println() {
  printf("\n");
  fflush(stdout);
}
*/

void *_alloc(int size) {
  void *result = malloc(size);
  if (result == NULL) {
      printf("malloc failed\n");
      exit(1);
  }
  return result;
}

// allocate memory for a string, copy the string to the allocated memory
// return the memory address of the allocated memory
char *String(char *s) {
  char *result = _alloc(strlen(s) + 1); //+1 for the zero-terminator

  strcpy(result, s);
  return result;
}

void free_str(char *s) {
  free(s);
}

char *Int2str(int n) {
  char *result = _alloc(12); // 12 is the max length of an int

  sprintf(result, "%d", n);
  return result;
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

int _get_start_index(int start, char *s) {
  if (start < 0) {
    return strlen(s) + start;
  } else if (start > strlen(s)) {
    return strlen(s);
  } else {
    return start;
  }
}

int _get_stop_index(int stop, char *s) {
  if (stop < 0) {
    return strlen(s) + stop;
  } else if (stop > strlen(s)) {
    return strlen(s) - 1;
  } else {
    return stop;
  }
}

char *Substr(char *s, int begin, int end) {
  /*if (begin < 0) {
    printf("invalid start or end index\n");
    exit(1);
  }*/
  int start = _get_start_index(begin, s);
  int stop = _get_stop_index(end, s);

  char *result = _alloc(stop - start + 2); //+1 for the zero-terminator

  strncpy(result, s + start, stop - start + 1);
  result[stop - start + 1] = '\0';
  return result;
}

char *Reverse(char *s) {
  char *result = _alloc(strlen(s) + 1); //+1 for the zero-terminator

  int i;
  for (i = 0; i < strlen(s); i++) {
    result[i] = s[strlen(s) - i - 1];
  }
  result[strlen(s)] = '\0';
  return result;
}

char *_case(char *s, int begin, int end, int upper) {
  int start = _get_start_index(begin, s);
  int stop = _get_stop_index(end, s);

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

int len(char *s) {
  return strlen(s);
}

int addr(void *p) {
  return (int)p;
}

char *addr2str(int n) {
  return (char *)n;
}

Array *Array_new(int size) {
  Array *result = _alloc(sizeof(Array));

  result->size = size;
  result->capacity = size;
  result->data = _alloc(result->capacity * sizeof(int));
  result->types = _alloc(result->capacity * sizeof(type));
  return result;
}

void put(Array *a, int i, int n, type t) {
  if (i < 0 || i >= a->size) {
    printf("index out of bounds\n");
    exit(1);
  }
  a->data[i] = n;
  a->types[i] = t;
}

int get(Array *a, int i) {
  if (i < 0 || i >= a->size) {
    printf("index out of bounds\n");
    exit(1);
  }
  return a->data[i];
}

char *get_type(Array *a, int i) {
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

void _array_resize(Array *a) {
  a->capacity *= 2;
  a->data = realloc(a->data, a->capacity * sizeof(int));
  a->types = realloc(a->types, a->capacity * sizeof(type));
}

void push(Array *a, int n, type t) {
  if (a->size == a->capacity) {
    _array_resize(a);
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
    a->data = realloc(a->data, a->capacity * sizeof(int));
    a->types = realloc(a->types, a->capacity * sizeof(type));
  }
  return result;
}

int size(Array *a) {
  return a->size;
}

void free_array(Array *a) {
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
    a->capacity /= 2;
    a->data = realloc(a->data, a->capacity * sizeof(int));
    a->types = realloc(a->types, a->capacity * sizeof(type));
  }
  return result;
}

int unshift(Array *a, int n, type t) {
  if (a->size == a->capacity) {
    _array_resize(a);
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
