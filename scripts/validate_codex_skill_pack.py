#!/usr/bin/env python3

import sys

from validate_codex_plugin_target import validate as validate_plugin
from validate_codex_project_target import validate as validate_project


def main():
    errors = [*validate_project(), *validate_plugin()]
    if errors:
        for error in errors:
            print(error)
        sys.exit(1)
    print("Legacy Codex validation alias passed both project and plugin contracts.")


if __name__ == "__main__":
    main()
