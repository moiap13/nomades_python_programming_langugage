import sys
import os

print(sys.path)
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
print(sys.path)

import callee

callee.say_hello()
