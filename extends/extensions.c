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

void *_realloc(void *p, int size) {
  void *result = realloc(p, size);
  if (result == NULL) {
      printf("realloc failed\n");
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

int _get_start_index(int start, int len) {
  if (start < 0) {
    return len + start;
  } else if (start > len) {
    return len;
  } else {
    return start;
  }
}

int _get_stop_index(int stop, int len) {
  if (stop < 0) {
    return len + stop;
  } else if (stop > len) {
    return len - 1;
  } else {
    return stop;
  }
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

char *append(char *s, char *s2) {
  char *r = (char *)_realloc(s, strlen(s) + strlen(s2) + 1);

  //strcpy(r, s);
  strcat(r, s2);
  return r;
}

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
void insert(int i, type t, int n, Array *a) {
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
