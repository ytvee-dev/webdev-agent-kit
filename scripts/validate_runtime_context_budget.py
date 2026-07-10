#!/usr/bin/env python3

import runpy
from pathlib import Path

VALIDATOR = Path(__file__).with_name("validate_context_budgets.py")


if __name__ == "__main__":
    runpy.run_path(str(VALIDATOR), run_name="__main__")
