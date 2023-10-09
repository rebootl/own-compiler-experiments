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

  char *sc = String(s);
  assert_equal_str(sc, "My String.", "String copy");
  free_str(sc);

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

  assert_equal_str(Revstr(s3), "dlroWolleH", "Revstr");

  assert_equal_str(Upper(s1, 2, 3), "HeLLo", "Upper");
  char *s10 = Upper(s3, 0, -1);
  assert_equal_str(Lower(s10, 0, 2), "helLOWORLD", "Lower");

  assert_equal_int(len(s2), 5, "len");
  assert_equal_int(len(s4), 3, "len");
  assert_equal_int(len(s7), 1, "len");

  //print(s3); // prints HelloWorld
  char *s11 = append(s3, " World");
  assert_equal_str(s11, "HelloWorld World", "append");

  Array *a = Array_new(5);

  put(0, INT, 42, a);
  put(1, INT, 43, a);
  put(2, INT, 44, a);
  int a0 = get(0, a); // 42
  assert_equal_int(a0, 42, "Array");
  int aun = get(3, a); // undefined
  assert_equal_int(aun, 0, "Array");
  //int a10 = get(a, 10); // out of bounds
  put(3, STRING, addr(String("Hi")), a);
  assert_equal_str(addr2str(get(3, a)), "Hi", "Array");

  printf("%d\n", addr(String("Hello"))); // prints 0x7f8e2b402a60

  push(INT, 45, a);
  assert_equal_int(get(5, a), 45, "Array push");

  assert_equal_str(get_type(0, a), "INT", "Array get_type");
  assert_equal_str(get_type(3, a), "STRING", "Array get_type");

  Array *b = Array_new(2);
  assert_equal_str(stringify(b), "[ 0, 0 ]", "Array empty");
  assert_equal_str(stringify(a), "[ 42, 43, 44, \"Hi\", 0, 45 ]", "Array stringify");
  push(ARRAY, addr(b), a);
  assert_equal_str(stringify(a), "[ 42, 43, 44, \"Hi\", 0, 45, [ 0, 0 ] ]", "Array push");
  put(0, INT, 42, b);
  assert_equal_str(stringify(a), "[ 42, 43, 44, \"Hi\", 0, 45, [ 42, 0 ] ]", "Array put");

  //assert_equal_int(shift(a), 42, "shift result");
  //assert_equal_str(stringify(a), "[ 43, 44, \"Hi\", 0, 45, [ 42, 0 ] ]", "Array shift");

  //unshift(a, 42, INT);
  //assert_equal_str(stringify(a), "[ 42, 43, 44, \"Hi\", 0, 45, [ 42, 0 ] ]", "Array unshift");

  Array *c = Slice(1, 3, a);
  assert_equal_str(stringify(c), "[ 43, 44, \"Hi\" ]", "Array slice");

  insert(4, INT, 43, a);
  assert_equal_str(stringify(a), "[ 42, 43, 44, \"Hi\", 43, 0, 45, [ 42, 0 ] ]", "Array insert");

  remove_at(3, a);
  assert_equal_str(stringify(a), "[ 42, 43, 44, 43, 0, 45, [ 42, 0 ] ]", "Array remove_at");

  Array *d = Copy(a);
  assert_equal_str(stringify(d), "[ 42, 43, 44, 43, 0, 45, [ 42, 0 ] ]", "Array copy");

  reverse(d);
  assert_equal_str(stringify(d), "[ [ 42, 0 ], 45, 0, 43, 44, 43, 42 ]", "Array reverse");

  remove_at(0, d);
  assert_equal_str(stringify(d), "[ 45, 0, 43, 44, 43, 42 ]", "Array shift");
  sort(d);
  assert_equal_str(stringify(d), "[ 0, 42, 43, 43, 44, 45 ]", "Array sort");

  Array *e = Array_new(5);
  put(0, STRING, addr("pe"), e);
  put(1, STRING, addr("De"), e);
  put(2, STRING, addr("al"), e);
  put(3, STRING, addr("be"), e);
  put(4, STRING, addr("Ar"), e);
  assert_equal_str(stringify(e), "[ \"pe\", \"De\", \"al\", \"be\", \"Ar\" ]", "Array strings");
  sort(e);
  assert_equal_str(stringify(e), "[ \"Ar\", \"De\", \"al\", \"be\", \"pe\" ]", "Array strings sort");


  free_array(a);

  return 0;
}
