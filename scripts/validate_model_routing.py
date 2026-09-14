#!/usr/bin/env python3
"""Check GPT instruction contracts and real packaged installer behavior, offline."""

import argparse
import json
import subprocess
import sys
import tempfile
from pathlib import Path

from test_model_routing import request

ROOT = Path(__file__).resolve().parents[1]
HELPER = "skills/project-onboarding-adapter/scripts/configure_gpt_agents.py"
POLICY = "common/codex-model-routing-policy.md"
BOOTSTRAP = "skills/project-onboarding-adapter/references/codex-model-bootstrap.md"
TEMPLATE = "templates/project/model-routing-profile.md"


def source_checks():
    errors = []
    markers = {
        "AGENTS.md": [POLICY, "before broad reading"],
        "adapters/codex.md": [POLICY, "codex-model-bootstrap.md"],
        "skills/project-onboarding-adapter/SKILL.md": [
            "Optional GPT Role Setup",
            "Plan Mode",
            "explicit",
        ],
        POLICY: [
            "wdk_lookup",
            "wdk_worker",
            "wdk_complex",
            "wdk_reviewer",
            "Do not forward the full parent transcript",
            "do not\nreset the shared retry budget",
            "No silent expensive fallback",
            "text-only",
            "self-review",
        ],
        BOOTSTRAP: [
            "standalone",
            "registered",
            "--apply --approve",
            "--rollback",
            "model/list",
            "explicit exception",
            "runtime metadata",
            "global collisions",
        ],
        TEMPLATE: [
            "activation-unverified",
            "configuration\nfingerprint",
            "No fixed savings promise",
        ],
        "skills/project-context-adapter/SKILL.md": ["Model Routing Drift", "stale"],
        "skills/webdev-kit-updater/SKILL.md": [
            "Host Model Configuration Boundary",
            "backups",
        ],
    }
    for relative, required in markers.items():
        text = (ROOT / relative).read_text(encoding="utf-8-sig")
        for marker in required:
            if marker not in text:
                errors.append(f"{relative}: missing contract {marker!r}")
    body = (ROOT / POLICY).read_text().split("\n---\n", 1)[1]
    if len(body.split()) > 550:
        errors.append("Routing policy exceeds its 550-word progressive-load budget")
    suite = json.loads((ROOT / "evals/model-routing-evals.json").read_text())
    version = json.loads((ROOT / "bundle-manifest.json").read_text())["version"]
    if suite["version"] != version or suite["eval_type"] != "model-routing":
        errors.append("Model routing eval metadata is inconsistent")
    ids = [c.get("id") for c in suite["cases"]]
    required_ids = {
        "no-consent",
        "plan-only",
        "unsupported-client",
        "unknown-catalog",
        "bounded-work",
        "escalation",
        "environment-failure",
        "review-isolation",
        "image-capability",
        "activation-proof",
        "update-drift",
        "measured-cost",
        "approved-native-gate",
        "pre-setup-no-spawn",
        "untrusted-config",
        "gate-conflict",
        "scoped-repair",
    }
    if set(ids) != required_ids or len(ids) != len(set(ids)):
        errors.append("Routing eval coverage is incomplete or duplicated")
    for case in suite["cases"]:
        if not case.get("prompt") or len(case.get("expected", [])) < 2:
            errors.append(f"Invalid routing eval case: {case.get('id')}")
    return errors


def generated_checks():
    errors = []
    manifest = json.loads((ROOT / "bundle-manifest.json").read_text())
    for target in (*manifest["targets"], *manifest["target_aliases"]):
        generated = ROOT / "dist" / target
        canonical = manifest["target_aliases"].get(target, target)
        for relative in (HELPER, POLICY, BOOTSTRAP, TEMPLATE):
            if not (generated / relative).is_file():
                errors.append(f"dist/{target}: missing {relative}")
        if errors:
            continue
        if (generated / HELPER).read_bytes() != (ROOT / HELPER).read_bytes():
            errors.append(f"dist/{target}: installer differs from source")
        if (generated / ".codex").exists() or (generated / "project").exists():
            errors.append(f"dist/{target}: contains installed host configuration")
        with tempfile.TemporaryDirectory() as temp:
            host = Path(temp)
            # Invoke the actual shipped helper, with only native installed markers.
            (host / ".agents/adapters").mkdir(parents=True)
            entry = generated / "AGENTS.md"
            if entry.is_file():
                (host / ".agents/AGENTS.md").write_bytes(entry.read_bytes())
            (host / ".agents/adapters" / f"{canonical}.md").write_bytes(
                (generated / "adapters" / f"{canonical}.md").read_bytes()
            )
            req = host / "request.json"
            req.write_text(json.dumps(request()))
            command = [
                sys.executable,
                str(generated / HELPER),
                "--root",
                temp,
                "--request",
                str(req),
                "--apply",
                "--approve",
            ]
            result = subprocess.run(command, capture_output=True, text=True)
            if canonical == "codex":
                if (
                    result.returncode
                    or json.loads(result.stdout).get("activation") != "unverified"
                ):
                    errors.append(
                        f"dist/{target}: packaged setup failed: {result.stderr}"
                    )
                activation_request = request()
                activation_request["activation"] = {
                    "config_key": "features.multi_agent",
                    "schema_evidence": "Synthetic installed-schema fixture",
                    "allow_enable": True,
                }
                req.write_text(json.dumps(activation_request))
                activated = subprocess.run(command, capture_output=True, text=True)
                inspected = subprocess.run(
                    [
                        sys.executable,
                        str(generated / HELPER),
                        "--root",
                        temp,
                        "--inspect",
                    ],
                    capture_output=True,
                    text=True,
                )
                if activated.returncode or inspected.returncode:
                    errors.append(
                        f"dist/{target}: packaged activation/inspection failed"
                    )
                else:
                    observation = json.loads(inspected.stdout)
                    if (
                        observation["native_gate"] != "enabled-in-project-config"
                        or observation["activation"] != "unverified"
                        or len(observation["roles"]) != 4
                    ):
                        errors.append(
                            f"dist/{target}: configuration/runtime boundary lost"
                        )
                repeat = subprocess.run(command, capture_output=True, text=True)
                if (
                    repeat.returncode
                    or json.loads(repeat.stdout).get("status") != "unchanged"
                ):
                    errors.append(f"dist/{target}: packaged setup is not idempotent")
            elif result.returncode == 0 or (host / ".codex").exists():
                errors.append(
                    f"dist/{target}: unsupported client wrote Codex configuration"
                )
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--generated", action="store_true")
    parser.add_argument("--skip-unit-tests", action="store_true")
    args = parser.parse_args()
    errors = source_checks()
    if args.generated:
        errors += generated_checks()
    if errors:
        print("\n".join(errors))
        return 1
    if not args.skip_unit_tests:
        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "unittest",
                "discover",
                "-s",
                "scripts",
                "-p",
                "test_model_routing.py",
            ],
            cwd=ROOT,
        )
        if result.returncode:
            return result.returncode
    print(
        "GPT routing contracts and offline configuration checks passed; live model execution is not claimed."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
