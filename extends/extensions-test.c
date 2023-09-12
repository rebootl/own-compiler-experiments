/* c extensions

  main file, for testing

*/
#include <stdio.h>  // for printf
#include <stdlib.h> // for malloc, free

#include "extensions.h"

int main(void) {

  print_i(42); // prints 42
  printf("\n");

  //println_i(43); // prints 42\n
  //println_i(0); // prints 0\n

  print("Hello"); // prints Hello

  //println("Hello"); // prints Hello\n
  println(); // prints \n

  char *s = allocate_str("My String.");
  print(s); // prints My String.
  println(); // prints \n
  free_str(s);

  char *si = int_to_str(42);
  print(si); // prints 42
  println(); // prints \n

  /* test concat, string concatenation */
  char *s1 = "Hello";
  char *s2 = "World";
  char *s3 = concat(s1, s2);
  printf("%s\n", s3); // prints HelloWorld
  free(s3);

  return 0;
}
