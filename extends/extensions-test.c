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

  char *s4 = substr(s1, 1, 3);
  printf("%s\n", s4); // prints ell
  char *s5 = substr(s3, 4, 6);
  printf("%s\n", s5); // prints oWo
  char *s6 = substr(s3, 2, -2); // negative indices count from the end
  printf("%s\n", s6); // prints lloWorl

  char *s7 = substr(s2, 0, 0);
  printf("%s\n", s7); // prints W
  char *s8 = substr(s2, 2, 10);
  printf("%s\n", s8); // prints rld

  char *s9 = substr(s3, -2, -1);
  printf("%s\n", s9); // prints ld

  printf("%s\n", reverse(s3)); // prints dlroWolleH

  printf("%s\n", uppercase(s1, 2, 3)); // prints HeLLo
  char *s10 = uppercase(s3, 0, -1);
  printf("%s\n", lowercase(s10, 0, 2)); // prints helLOWORLD

  printf("%d\n", len(s1)); // prints 5
  printf("%d\n", len(s3)); // prints 10
  printf("%d\n", len(s6)); // prints 6

  free(s3);
  free(s4);
  free(s5);
  free(s6);
  free(s7);
  free(s8);
  free(s9);
  free(s10);

  return 0;
}
