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
void println_i(int n) {
  printf("%d\n", n);
  fflush(stdout);
}

void print(char *s) {
  printf("%s", s);
  fflush(stdout);
}

void println() {
  printf("\n");
  fflush(stdout);
}

void *_alloc(int size) {
  void *result = malloc(size);
  if (result == NULL) {
      printf("malloc failed\n");
      exit(1);
  }
  return result;
}

char *allocate_str(char *s) {
  char *result = _alloc(strlen(s) + 1); //+1 for the zero-terminator

  strcpy(result, s);
  return result;
}

void free_str(char *s) {
  free(s);
}

char *int_to_str(int n) {
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
char *concat(char *s1, char *s2) {
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

char *substr(char *s, int begin, int end) {
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

char *reverse(char *s) {
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

char *uppercase(char *s, int begin, int end) {
  return _case(s, begin, end, 1);
}

char *lowercase(char *s, int begin, int end) {
  return _case(s, begin, end, 0);
}

int len(char *s) {
  return strlen(s);
}
