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

char *allocate_str(char *s) {
  char *result = malloc(strlen(s) + 1); //+1 for the zero-terminator
  if (result == NULL) {
      printf("malloc failed\n");
      exit(1);
  }
  strcpy(result, s);
  return result;
}

void free_str(char *s) {
  free(s);
}

char *int_to_str(int n) {
  char *result = malloc(12); // 12 is the max length of an int
  if (result == NULL) {
      printf("malloc failed\n");
      exit(1);
  }
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
  char *result = malloc(strlen(s1) + strlen(s2) + 1); //+1 for the zero-terminator
  if (result == NULL) {
      printf("malloc failed\n");
      exit(1);
  }
  strcpy(result, s1);
  strcat(result, s2);
  return result;
}

char *substr(char *s, int start, int end) {
  if (start < 0 || end == 0) {
    printf("invalid start or end index\n");
    exit(1);
  }
  int stop;
  if (end < 0) {
    stop = strlen(s) + end - 1;
  } else {
    stop = end;
  }

  char *result = malloc(stop - start + 2); //+1 for the zero-terminator
  if (result == NULL) {
      printf("malloc failed\n");
      exit(1);
  }
  strncpy(result, s + start, stop - start + 1);
  result[stop - start + 1] = '\0';
  return result;
}

int len(char *s) {
  return strlen(s);
}
