from __future__ import annotations

import subprocess
import sys


COMMANDS = [
    [sys.executable, "-m", "unittest", "discover", "-s", "tests/unit", "-t", ".", "-p", "*_spec.py", "-v"],
    [sys.executable, "-m", "unittest", "discover", "-s", "tests/integration", "-t", ".", "-p", "*_it.py", "-v"],
]


for command in COMMANDS:
    subprocess.run(command, check=True)

