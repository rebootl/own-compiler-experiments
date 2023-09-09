
// concatenate two strings

#include <stdio.h>
#include <string.h>

int main(void)
{
    char s1[100] = "Hello";

    char s2[] = "World";

    strcat(s1, s2);


    printf("%s\n", s1);

    return 0;
}
