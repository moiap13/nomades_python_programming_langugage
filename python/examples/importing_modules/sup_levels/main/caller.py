import sys, os
ROOT_PATH: str = os.path.dirname(os.path.dirname(__file__))
sys.path.append(ROOT_PATH)

import callee as c

c.say_hello()