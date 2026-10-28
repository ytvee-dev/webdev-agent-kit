"""One state resolver for project capture, learning and exchange."""
import argparse
import json
import os
from pathlib import Path


def state_root(project, state=None):
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--state")
    args, _ = parser.parse_known_args()
    override = state or args.state or os.environ.get("AGENT_LEARNING_STATE")
    return (Path(override).expanduser() if override else Path(project).expanduser().resolve() / ".agents/learning").resolve()


def check_owner(project, state):
    descriptor = Path(state) / "project.json"
    if descriptor.is_file():
        config = json.loads(descriptor.read_text(encoding="utf-8"))
        owner = config.get("project_root")
        if owner and Path(owner).resolve() != Path(project).resolve() and (Path(owner).exists() or Path(state).resolve() != Path(project).resolve() / ".agents/learning"):
            raise ValueError("Selected state belongs to another project; explicitly migrate it")
        return config
    return None
