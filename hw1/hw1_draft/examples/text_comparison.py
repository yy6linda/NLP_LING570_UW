
import difflib
import sys

with open('./ex2.tok', 'r') as hosts0:
   with open('./ex2.tok2', 'r') as hosts1:
      diff = difflib.unified_diff(
         hosts0.readlines(),
         hosts1.readlines(),
         fromfile='hosts0',
         tofile='hosts1',
      )
      for line in diff:
         sys.stdout.write(line)
