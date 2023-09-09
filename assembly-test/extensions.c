/* c extension to concat two strings
*/

#include <stdio.h>  // for printf
#include <string.h> // for strlen, strcpy, strcat
#include <stdlib.h> // for malloc

#include "extensions.h"

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
