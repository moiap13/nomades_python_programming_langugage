import sys, os

parent_folder = os.path.dirname(os.path.dirname(__file__))
module_path = os.path.join(parent_folder, "modules")

sys.path.append(module_path)

from callee import say_hello

say_hello()
