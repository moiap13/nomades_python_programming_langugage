import sys, os

CURR_DIR: str = os.path.dirname(__file__)
sys.path.append(os.path.dirname(CURR_DIR))

from callee import say_hello

say_hello()
