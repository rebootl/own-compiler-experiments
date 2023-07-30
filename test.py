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
  [ 'programs/06-inc-dec.src', '', 0 ],
  [ 'programs/07-exit-inc.src', '', 6 ],
  [ 'programs/08-print.src', '55', 0 ],
  [ 'programs/09-print-inc.src', '56', 0 ],
  [ 'programs/10-println.src', '\n', 0 ],
  [ 'programs/11-print-println.src', '55\n65\n', 0 ],
  [ 'programs/12-print-not.src', '0', 0 ],
]

for case in CASES:
  # remove .src extension
  name = case[0][:-4]

  # build program
  os.system('./compiler.py ' + case[0] + ' > out.asm')
  os.system('nasm -f elf32 out.asm -o out.o')
  os.system('ld -m elf_i386 -o out out.o')

  # run program
  p = subprocess.Popen('./out', stdout=subprocess.PIPE, stderr=subprocess.PIPE)
  stdout, stderr = p.communicate()

  # check exit code
  if p.returncode != case[2]:
    print('FAIL: ' + name + ' exit code ' + str(p.returncode) + ' != ' + str(case[2]))
    exit(1)

  # check stdout
  if stdout.decode('utf-8') != case[1]:
    print('FAIL: ' + name + ' stdout "' + stdout.decode('utf-8') + '" != "' + case[1] + '"')
    exit(1)

  print('PASS: ' + name)
