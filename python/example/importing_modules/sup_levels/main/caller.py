import sys
import os
from pathlib import Path

# ROOT_DIR: str = os.path.dirname(os.path.dirname(__file__))
ROOT_DIR = Path(__file__).parent.parent

sys.path.append(str(ROOT_DIR))

import callee

callee.say_hello()