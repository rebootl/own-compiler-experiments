/* c extensions

  main file, for testing

*/
#include <stdio.h>  // for printf
#include <stdlib.h> // for malloc, free
#include <string.h> // for strcmp

#include "extensions.h"

int assert_equal_str(char *result, char *expected, char *msg) {
  if (strcmp(result, expected) == 0) {
    printf("OK: %s\n", msg);
    return 1;
  } else {
    printf("FAIL: %s\n", msg);
    printf("  expected: %s\n", expected);
    printf("  got:      %s\n", result);
    return 0;
  }
}

int assert_equal_int(int result, int expected, char *msg) {
  if (result == expected) {
    printf("OK: %s\n", msg);
    return 1;
  } else {
    printf("FAIL: %s\n", msg);
    printf("  expected: %d\n", expected);
    printf("  got:      %d\n", result);
    return 0;
  }
}

int main(void) {

  print_i(42); // prints 42
  print("\n");

  print("Hello"); // prints Hello
  print("\n");

  char *s = String("My String.");
  assert_equal_str(s, "My String.", "String");

  char *c = String(s);
  assert_equal_str(c, "My String.", "String copy");
  free_str(s);

  char *si = Int2str(42);
  assert_equal_str(si, "42", "Int2str");

  /* test concat, string concatenation */
  char *s1 = "Hello";
  char *s2 = "World";
  char *s3 = Concat(s1, s2);
  assert_equal_str(s3, "HelloWorld", "Concat");

  char *s4 = Substr(s1, 1, 3);
  assert_equal_str(s4, "ell", "Substr");
  char *s5 = Substr(s3, 4, 6);
  assert_equal_str(s5, "oWo", "Substr");
  char *s6 = Substr(s3, 2, -2); // negative indices count from the end
  assert_equal_str(s6, "lloWorl", "Substr");

  char *s7 = Substr(s2, 0, 0);
  assert_equal_str(s7, "W", "Substr");
  char *s8 = Substr(s2, 2, 10);
  assert_equal_str(s8, "rld", "Substr");

  char *s9 = Substr(s3, -2, -1);
  assert_equal_str(s9, "ld", "Substr");

  assert_equal_str(Reverse(s3), "dlroWolleH", "Reverse");

  assert_equal_str(Upper(s1, 2, 3), "HeLLo", "Upper");
  char *s10 = Upper(s3, 0, -1);
  assert_equal_str(Lower(s10, 0, 2), "helLOWORLD", "Lower");

  assert_equal_int(len(s2), 5, "len");
  assert_equal_int(len(s4), 3, "len");
  assert_equal_int(len(s7), 1, "len");

  Array *a = Array_new(5);

  put(a, 0, 42, INT);
  put(a, 1, 43, INT);
  put(a, 2, 44, INT);
  int a0 = get(a, 0); // 42
  assert_equal_int(a0, 42, "Array");
  int aun = get(a, 3); // undefined
  assert_equal_int(aun, 0, "Array");
  //int a10 = get(a, 10); // out of bounds
  put(a, 3, addr(String("Hi")), STRING);
  assert_equal_str(addr2str(get(a, 3)), "Hi", "Array");

  printf("%d\n", addr(String("Hello"))); // prints 0x7f8e2b402a60

  push(a, 45, INT);
  assert_equal_int(get(a, 5), 45, "Array push");

  assert_equal_str(get_type(a, 0), "INT", "Array get_type");
  assert_equal_str(get_type(a, 3), "STRING", "Array get_type");

  Array *b = Array_new(2);
  print_array(a);
  push(a, addr(b), ARRAY);
  print_array(a);
  put(b, 0, 42, INT);
  print_array(a);

  assert_equal_int(shift(a), 42, "Array shift");
  print_array(a);

  unshift(a, 42, INT);
  print_array(a);

  free_array(a);

  return 0;
}
