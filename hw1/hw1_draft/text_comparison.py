
import difflib
import sys

with open('./test.tok', 'r') as hosts0:
   with open('./file.tok.gold', 'r') as hosts1:
      diff = difflib.unified_diff(
         hosts0.readlines(),
         hosts1.readlines(),
         fromfile='hosts0',
         tofile='hosts1',
      )
      for line in diff:
         sys.stdout.write(line)
