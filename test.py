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
  #[ 'programs/06-inc-dec.src', '', 0 ],
  #[ 'programs/07-exit-inc.src', '', 6 ],
  [ 'programs/08-print.src', '55', 0 ],
  #[ 'programs/09-print-inc.src', '56', 0 ],
  [ 'programs/10-println.src', '\n', 0 ],
  [ 'programs/11-print-println.src', '55\n65\n', 0 ],
  [ 'programs/12-add.src', '4', 0 ],
  [ 'programs/13-add-sub.src', '6\n2\n', 0 ],
  [ 'programs/13.1-mul.src', '4\n25\n', 0 ],
  [ 'programs/14-collapse-comments.src', '6\n5\n', 0 ],
  [ 'programs/15-vars.src', '15\n9', 0 ],
  [ 'programs/16-vars-set.src', '20', 0 ],
  [ 'programs/17-block.src', '25', 0 ],
  [ 'programs/18-eq.src', '101101', 0 ],
  [ 'programs/19-ne.src', '0100', 0 ],
  [ 'programs/20-gt-lt.src', '001110100', 0 ],
  [ 'programs/21-ge-le.src', '10111100', 0 ],
  [ 'programs/22-and-or.src', '10001110', 0 ],
  [ 'programs/23-not-combs.src', '01100', 0 ],
  [ 'programs/24-if.src', '703', 0 ],
  [ 'programs/25-if-else.src', '125464', 0 ],
  [ 'programs/26-while.src', '0012341012342012343012344012345', 0 ],
  [ 'programs/27-fib.src', '23581321345589144', 0 ],
  [ 'programs/28-fac.src', '3628800', 0 ],
  [ 'programs/29-fac-overflow.src', '', 99 ],
  [ 'programs/30-while-break.src', '98765', 0 ],
  [ 'programs/31-while-continue.src', '9876540', 0 ],
  [ 'programs/32-function.src', '1020', 0 ],
  #[ 'programs/12-print-not.src', '0', 0 ],
]

for case in CASES:
  # remove .src extension
  name = case[0][:-4]

  # build program
  # -> check success and break if fail
  # -> check errors
  os.system('./compiler.py ' + case[0])
  os.system('nasm -f elf32 out.asm -o out.o')
  os.system('ld -m elf_i386 -o out out.o')

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
