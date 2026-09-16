import sys, os
ROOT_DIR: str = os.path.dirname(os.path.dirname(__file__))
sys.path.append(ROOT_DIR)

from callee import say_hello

say_hello()
