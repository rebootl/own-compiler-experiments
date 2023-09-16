#!/usr/bin/env python
#
# tests

import os
import subprocess

CASES = [
  [ 'programs/01-exit-empty.src', '', 0 ],
  [ 'programs/02-exit-default.src', '', 0 ],
  [ 'programs/03-exit-zero.src', '', 0 ],
  [ 'programs/04-exit-five.src', '', 5 ],
  [ 'programs/05-exit-twentyfive.src', '', 25 ],
  [ 'programs/08-print.src', '55', 0 ],
  [ 'programs/09-print-signed.src', '-552147483647-2147483648', 0 ],
  [ 'programs/10-println.src', '\n', 0 ],
  [ 'programs/11-print-println.src', '55\n65\n', 0 ],
  [ 'programs/11.1-println-value.src', '10\n6515\n12\n15\n', 0 ],
  [ 'programs/12-add.src', '4', 0 ],
  [ 'programs/12.1-add-signed.src', '40-47', 0 ],
  [ 'programs/13-add-sub.src', '6\n2\n', 0 ],
  [ 'programs/13.0-add-sub-signed.src', '-4\n2\n8\n-8\n', 0 ],
  [ 'programs/13.1-mul.src', '4\n75\n', 0 ],
  [ 'programs/13.2-mul-signed.src', '-4\n1\n-300\n-15\n', 0 ],
  [ 'programs/13.3-div.src', '501-5-6750', 0 ],
  [ 'programs/13.4-neg.src', '-1085-50', 0 ],
  [ 'programs/13.5-mod.src', '012050120-2-200-1-1', 0 ],
  [ 'programs/13.6-abs.src', '10103450350', 0 ],
  [ 'programs/13.7-overflow.src', '0101', 0 ],
  [ 'programs/14-collapse-comments.src', '6\n5\n', 0 ],
  [ 'programs/15-vars.src', '15\n9', 0 ],
  [ 'programs/16-vars-set.src', '20', 0 ],
  [ 'programs/17-block.src', '25', 0 ],
  [ 'programs/18-eq.src', '101101110', 0 ],
  [ 'programs/19-ne.src', '010001', 0 ],
  [ 'programs/20-gt-lt.src', '001110100\n01010\n10001', 0 ],
  [ 'programs/21-ge-le.src', '10111100\n0111\n1010', 0 ],
  [ 'programs/22-and-or.src', '10001110\n01110\n11111', 0 ],
  [ 'programs/23-not-combs.src', '0110000', 0 ],
  [ 'programs/24-if.src', '703', 0 ],
  [ 'programs/25-if-else.src', '125464', 0 ],
  [ 'programs/26-while.src', '0012341012342012343012344012345', 0 ],
  [ 'programs/27-fib.src', '23581321345589144', 0 ],
  [ 'programs/28-fac.src', '3628800', 0 ],
  [ 'programs/29-fac-overflow.src', '', 99 ],
  [ 'programs/30-while-break.src', '98765', 0 ],
  [ 'programs/31-while-continue.src', '9876540', 0 ],
  [ 'programs/32-function.src', '103010', 0 ],
  [ 'programs/33-function-return.src', '1030301030', 0 ],
  [ 'programs/34-function-args.src', '15\n20\n25\n510', 0 ],
  [ 'programs/35-function-recursion.src', '109876543210', 0 ],
  [ 'programs/36-function-recursion-fib.src', '01123581321345589', 0 ],
  [ 'programs/37-function-recursion-fac.src', '3628800', 0 ],
  [ 'programs/38-print-string.src', 'Hello World!', 0 ],
  [ 'programs/39-string-lit-var.src', 'My 1st string literal.FooMy 2nd string literal, longer.', 0 ],
  [ 'programs/40-string-lit-loop.src', 'AAAAA', 0 ],
  [ 'programs/41-fizzbuzz.src', '1\n2\nfizz\n4\nbuzz\nfizz\n7\n8\nfizz\nbuzz\n11\nfizz\n13\n14\nfizzbuzz\n', 0 ],
  [ 'programs/42-int_to_str.src', '123', 0 ],
]

for case in CASES:
  # remove .src extension
  name = case[0][:-4]

  # build program
  # -> check success and break if fail
  # -> check errors
  os.system('./compiler.py ' + case[0])
  os.system('nasm -f elf32 out.asm -o out.o')
  #os.system('ld -m elf_i386 -o out out.o')

  # gcc is needed when linking to libc/ c extensions

  os.system('gcc -no-pie -m32 -o out out.o extends/extensions.o')

  ## ^^ no-pie fixes ld errors:
  # /usr/bin/ld: out.o: warning: relocation in read-only section `.text'
  # /usr/bin/ld: warning: creating DT_TEXTREL in a PIE
  #
  # -static also fixes, but makes code noticeably slower, and big

  # run program
  p = subprocess.Popen('./out', stdout=subprocess.PIPE, stderr=subprocess.PIPE)
  stdout, stderr = p.communicate()

  # check exit code
  if p.returncode != case[2]:
    print('FAIL: ' + name + ' exit code ' + str(p.returncode) + ' != ' + str(case[2]))
    print('stdout: ' + stdout.decode('utf-8'))
    exit(1)

  # check stdout
  if stdout.decode('utf-8') != case[1]:
    print('FAIL: ' + name + ' stdout "' + stdout.decode('utf-8') + '" != "' + case[1] + '"')
    exit(1)

  print('PASS: ' + name)
