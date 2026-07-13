import sys, os
from pathlib import Path

# ROOT_DIR: str = os.path.dirname(os.path.dirname(__file__))
# MODULES_DIR: str = os.path.join(ROOT_DIR, "modules")
# sys.path.append(ROOT_DIR)
# sys.path.append(MODULES_DIR)

ROOT_DIR: Path = Path(__file__).parent.parent
MODULES_DIR: Path = ROOT_DIR / "modules"
sys.path.append(str(ROOT_DIR))
sys.path.append(str(MODULES_DIR))

import callee as c

c.say_hello()