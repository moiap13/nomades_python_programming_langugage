import sys, os

parent_folder = os.path.dirname(os.path.dirname(__file__))
# module_path = os.path.join(parent_folder, "modules")

sys.path.append(parent_folder)

from modules.callee import say_hello

say_hello()
