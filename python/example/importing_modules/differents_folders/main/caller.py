import os, sys
ROOT_DIR: str = os.path.dirname(os.path.dirname(__file__))
MODULES_DIR: str = os.path.join(ROOT_DIR, 'modules')
sys.path.append(ROOT_DIR)
sys.path.append(MODULES_DIR)

from callee import say_hello
say_hello()