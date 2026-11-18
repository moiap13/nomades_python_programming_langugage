import os, sys
ROOT_DIR: str = os.path.dirname(os.path.dirname(__file__))
#MODULES_DIR: str = os.path.join(ROOT_DIR, 'modules')
sys.path.append(ROOT_DIR)

from modules.callee import say_hello
say_hello()