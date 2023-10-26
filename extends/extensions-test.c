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

int assert_equal_float(float result, float expected, char *msg) {
  if (result == expected) {
    printf("OK: %s\n", msg);
    return 1;
  } else {
    printf("FAIL: %s\n", msg);
    printf("  expected: %f\n", expected);
    printf("  got:      %f\n", result);
    return 0;
  }
}

int main(void) {

  // Create

  Element *n = new_Nil();
  // print(n);
  assert_equal_str(str(n), "Nil", "Nil");

  Element *b = new_Bool(TRUE);
  // print(b);
  assert_equal_str(str(b), "True", "Bool");

  Element *i = new_Int(42);
  // print(i);
  assert_equal_int(i->el.value, 42, "Int el.");
  assert_equal_str(str(i), "42", "Int");

  Element *f = new_Float(42.42);
  // print(f);
  assert_equal_float(f->el.fvalue, 42.42, "Float el.");
  assert_equal_str(str(f), "42.419998", "Float");

  Element *s = new_String("Hello");
  // print(s);
  assert_equal_str(s->el.string, "Hello", "String el.");
  assert_equal_str(str(s), "Hello", "String");

  Element *a = new_Array(5);
  assert_equal_int(a->el.array->size, 5, "Array el.");
  assert_equal_int(a->el.array->capacity, 5, "Array el.");
  assert_equal_str(str(a), "[ Nil, Nil, Nil, Nil, Nil ]", "Array");

  // Manipulate

  append(s, new_String(" World"));
  assert_equal_str(str(s), "Hello World", "String append");
  append(s, new_String("!"));
  assert_equal_str(str(s), "Hello World!", "String append");
  append(s, new_String("!"));
  assert_equal_str(str(s), "Hello World!!", "String append");

  set(0, s, new_String("F"));
  assert_equal_str(str(s), "Fello World!!", "String set");

  set(0, a, new_Int(42));
  assert_equal_str(str(a), "[ 42, Nil, Nil, Nil, Nil ]", "Array set");
  set(3, a, new_Int(43));
  assert_equal_str(str(a), "[ 42, Nil, Nil, 43, Nil ]", "Array set");
  set(4, a, new_String("Hi"));
  assert_equal_str(str(a), "[ 42, Nil, Nil, 43, \"Hi\" ]", "Array set");

  append(a, new_Int(44));
  assert_equal_str(str(a), "[ 42, Nil, Nil, 43, \"Hi\", 44 ]", "Array append");

  set(-3, a, new_Int(45));
  assert_equal_str(str(a), "[ 42, Nil, Nil, 45, \"Hi\", 44 ]", "Array set");

  Element *a2 = new_Array(0);
  assert_equal_str(str(a2), "[  ]", "Array empty");

  append(a2, new_Int(42));
  append(a2, new_Array(3));
  assert_equal_str(str(a2), "[ 42, [ Nil, Nil, Nil ] ]", "Array append");

  Element *e = pop(a);
  assert_equal_str(str(e), "44", "Array pop");
  assert_equal_str(str(a), "[ 42, Nil, Nil, 45, \"Hi\" ]", "Array pop");
  
  Element *re = remove_at(1, a);
  assert_equal_str(str(re), "Nil", "Array remove_el");
  assert_equal_str(str(a), "[ 42, Nil, 45, \"Hi\" ]", "Array remove_el");

  insert_at(1, a, new_Int(43));
  assert_equal_str(str(a), "[ 42, 43, Nil, 45, \"Hi\" ]", "Array insert_el");

  // Destroy

  // destroy(a);
  // destroy(s);
  // destroy(f);
  // destroy(i);
  // destroy(b);
  // destroy(n);

  // Convert

  Element *b1 = to_bool(new_Int(42));
  assert_equal_str(str(b1), "True", "int to_bool");

  Element *b2 = to_bool(new_Int(0));
  assert_equal_str(str(b2), "False", "int 0 to_bool");

  Element *b3 = to_bool(new_Float(42.42));
  assert_equal_str(str(b3), "True", "float to_bool");

  Element *b4 = to_bool(new_Float(0.0));
  assert_equal_str(str(b4), "False", "float 0.0 to_bool");

  Element *i1 = to_int(new_Float(42.42));
  assert_equal_int(i1->el.value, 42, "float to_int");

  Element *i2 = to_int(new_Float(0.0));
  assert_equal_int(i2->el.value, 0, "float 0.0 to_int");

  Element *f1 = to_float(new_Int(42));
  assert_equal_float(f1->el.fvalue, 42.0, "int to_float");

  Element *f2 = to_float(new_Int(0));
  assert_equal_float(f2->el.fvalue, 0.0, "int 0 to_float");

  Element *sb1 = to_string(new_Int(42));
  assert_equal_str(sb1->el.string, "42", "int to_string");

  Element *sb2 = to_string(new_Float(42.42));
  assert_equal_str(sb2->el.string, "42.419998", "float to_string");

  // Query

  Element *b7 = is_nil(new_Nil());
  assert_equal_str(str(b7), "True", "is_nil");

  Element *b8 = is_nil(new_Int(42));
  assert_equal_str(str(b8), "False", "is_nil");

  Element *l1 = len(new_String("Hello"));
  assert_equal_int(l1->el.value, 5, "len string");

  Element *l2 = len(new_Array(5));
  assert_equal_int(l2->el.value, 5, "len array");

  Element *e1 = get(1, new_String("Hello"));
  assert_equal_str(str(e1), "e", "get string");

  Element *e2 = get(3, a);
  assert_equal_str(str(e2), "45", "get array");

  // Math
  
  Element *r = add(new_Int(42), new_Int(43));
  assert_equal_int(r->el.value, 85, "add ints");

  Element *r2 = add(new_Float(42.42), new_Float(43.43));
  assert_equal_float(r2->el.fvalue, 85.85, "add floats");

  Element *r3 = sub(new_Int(42), new_Int(43));
  assert_equal_int(r3->el.value, -1, "sub ints");

  // Compare
  
  Element *s1 = new_String("Hello");
  Element *s2 = new_String("Hello");
  Element *b5 = eq(s1, s2);
  assert_equal_str(str(b5), "True", "eq strings");

  Element *s3 = new_String("Hello");
  Element *s4 = new_String("World");
  Element *b6 = eq(s3, s4);
  assert_equal_str(str(b6), "False", "eq strings");

  Element *r4 = eq(new_Int(42), new_Int(42));
  assert_equal_str(str(r4), "True", "eq ints");

  Element *r5 = eq(new_Float(42.42), new_Float(42.42));
  assert_equal_str(str(r5), "True", "eq floats");

  Element *r6 = lt(new_String("A"), new_String("B"));
  assert_equal_str(str(r6), "True", "lt strings");

  Element *r7 = lt(new_Float(42.42), new_Float(43.43));
  assert_equal_str(str(r7), "True", "lt floats");

  // Logic

  Element *r8 = _and(new_Bool(TRUE), new_Bool(TRUE));
  assert_equal_str(str(r8), "True", "and bools");

  Element *r9 = _and(new_Bool(TRUE), new_Bool(FALSE));
  assert_equal_str(str(r9), "False", "and bools");

  Element *r10 = _or(new_Bool(TRUE), new_Bool(FALSE));
  assert_equal_str(str(r10), "True", "or bools");

  Element *r11 = _or(new_Bool(FALSE), new_Bool(FALSE));
  assert_equal_str(str(r11), "False", "or bools");

  Element *r12 = _not(new_Bool(TRUE));
  assert_equal_str(str(r12), "False", "not bool");

  Element *r13 = _not(new_Bool(FALSE));
  assert_equal_str(str(r13), "True", "not bool");

  // print_i(42); // prints 42
  // print("\n");

  // print("Hello"); // prints Hello
  // print("\n");

  // char *s = String("My String.");
  // assert_equal_str(s, "My String.", "String");

  // char *sc = String(s);
  // assert_equal_str(sc, "My String.", "String copy");
  // free_str(sc);

  // char *si = Int2str(42);
  // assert_equal_str(si, "42", "Int2str");

  // /* test concat, string concatenation */
  // char *s1 = "Hello";
  // char *s2 = "World";
  // char *s3 = Concat(s1, s2);
  // assert_equal_str(s3, "HelloWorld", "Concat");

  // char *s4 = Substr(s1, 1, 3);
  // assert_equal_str(s4, "ell", "Substr");
  // char *s5 = Substr(s3, 4, 6);
  // assert_equal_str(s5, "oWo", "Substr");
  // char *s6 = Substr(s3, 2, -2); // negative indices count from the end
  // assert_equal_str(s6, "lloWorl", "Substr");

  // char *s7 = Substr(s2, 0, 0);
  // assert_equal_str(s7, "W", "Substr");
  // char *s8 = Substr(s2, 2, 10);
  // assert_equal_str(s8, "rld", "Substr");

  // char *s9 = Substr(s3, -2, -1);
  // assert_equal_str(s9, "ld", "Substr");

  // assert_equal_str(Revstr(s3), "dlroWolleH", "Revstr");

  // assert_equal_str(Upper(s1, 2, 3), "HeLLo", "Upper");
  // char *s10 = Upper(s3, 0, -1);
  // assert_equal_str(Lower(s10, 0, 2), "helLOWORLD", "Lower");

  // assert_equal_int(len(s2), 5, "len");
  // assert_equal_int(len(s4), 3, "len");
  // assert_equal_int(len(s7), 1, "len");

  // //print(s3); // prints HelloWorld
  // char *s11 = append(s3, " World");
  // assert_equal_str(s11, "HelloWorld World", "append");

  // Array *a = Array_new(5);

  // put(0, INT, 42, a);
  // put(1, INT, 43, a);
  // put(2, INT, 44, a);
  // int a0 = get(0, a); // 42
  // assert_equal_int(a0, 42, "Array");
  // int aun = get(3, a); // undefined
  // assert_equal_int(aun, 0, "Array");
  // //int a10 = get(a, 10); // out of bounds
  // put(3, STRING, addr(String("Hi")), a);
  // assert_equal_str(addr2str(get(3, a)), "Hi", "Array");

  // printf("%d\n", addr(String("Hello"))); // prints 0x7f8e2b402a60

  // push(INT, 45, a);
  // assert_equal_int(get(5, a), 45, "Array push");

  // assert_equal_str(get_type(0, a), "INT", "Array get_type");
  // assert_equal_str(get_type(3, a), "STRING", "Array get_type");

  // Array *b = Array_new(2);
  // assert_equal_str(stringify(b), "[ 0, 0 ]", "Array empty");
  // assert_equal_str(stringify(a), "[ 42, 43, 44, \"Hi\", 0, 45 ]", "Array stringify");
  // push(ARRAY, addr(b), a);
  // assert_equal_str(stringify(a), "[ 42, 43, 44, \"Hi\", 0, 45, [ 0, 0 ] ]", "Array push");
  // put(0, INT, 42, b);
  // assert_equal_str(stringify(a), "[ 42, 43, 44, \"Hi\", 0, 45, [ 42, 0 ] ]", "Array put");

  // //assert_equal_int(shift(a), 42, "shift result");
  // //assert_equal_str(stringify(a), "[ 43, 44, \"Hi\", 0, 45, [ 42, 0 ] ]", "Array shift");

  // //unshift(a, 42, INT);
  // //assert_equal_str(stringify(a), "[ 42, 43, 44, \"Hi\", 0, 45, [ 42, 0 ] ]", "Array unshift");

  // Array *c = Slice(1, 3, a);
  // assert_equal_str(stringify(c), "[ 43, 44, \"Hi\" ]", "Array slice");

  // insert(4, INT, 43, a);
  // assert_equal_str(stringify(a), "[ 42, 43, 44, \"Hi\", 43, 0, 45, [ 42, 0 ] ]", "Array insert");

  // remove_at(3, a);
  // assert_equal_str(stringify(a), "[ 42, 43, 44, 43, 0, 45, [ 42, 0 ] ]", "Array remove_at");

  // Array *d = Copy(a);
  // assert_equal_str(stringify(d), "[ 42, 43, 44, 43, 0, 45, [ 42, 0 ] ]", "Array copy");

  // reverse(d);
  // assert_equal_str(stringify(d), "[ [ 42, 0 ], 45, 0, 43, 44, 43, 42 ]", "Array reverse");

  // remove_at(0, d);
  // assert_equal_str(stringify(d), "[ 45, 0, 43, 44, 43, 42 ]", "Array shift");
  // sort(d);
  // assert_equal_str(stringify(d), "[ 0, 42, 43, 43, 44, 45 ]", "Array sort");

  // Array *e = Array_new(5);
  // put(0, STRING, addr("pe"), e);
  // put(1, STRING, addr("De"), e);
  // put(2, STRING, addr("al"), e);
  // put(3, STRING, addr("be"), e);
  // put(4, STRING, addr("Ar"), e);
  // assert_equal_str(stringify(e), "[ \"pe\", \"De\", \"al\", \"be\", \"Ar\" ]", "Array strings");
  // sort(e);
  // assert_equal_str(stringify(e), "[ \"Ar\", \"De\", \"al\", \"be\", \"pe\" ]", "Array strings sort");


  // free_array(a);

  return 0;
}
