
#include <stdio.h>

#include "scanner.h"
#include "parser.h"


int main(int argc, char** argv) {
  // char* test_str = "  123 + 4";

	char line[1024];

	while (1) {
	  printf("> ");

    if (!fgets(line, sizeof(line), stdin)) {
			printf("\n");
			break;
		}

		interpret(line);
  }

  return 0;
}
