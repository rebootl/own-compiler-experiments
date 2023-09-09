/* c extensions

  main file, for testing

*/
#include <stdio.h>  // for printf
#include <stdlib.h> // for malloc, free

#include "extensions.h"

int main(void) {

  /* test concat, string concatenation */

  char *s1 = "Hello";
  char *s2 = "World";
  char *s3 = concat(s1, s2);
  printf("%s\n", s3); // prints HelloWorld
  free(s3);

  return 0;
}
