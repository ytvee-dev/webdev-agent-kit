#!/usr/bin/env python3
"""Offline installer regressions. Catalog IDs are synthetic, not live models."""

import copy
import importlib.util
import json
import os
import re
import subprocess
import sys
import tempfile
import tomllib
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
HELPER = ROOT / "skills/project-onboarding-adapter/scripts/configure_gpt_agents.py"
SPEC = importlib.util.spec_from_file_location("configure_gpt_agents", HELPER)
kit = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(kit)


def request(fmt="standalone"):
    roles = {}
    for name in kit.ROLES:
        small = name in {"wdk_lookup", "wdk_worker"}
        roles[name] = {
            "model": "gpt-fixture-economy" if small else "gpt-fixture-capable",
            "effort": "low" if small else "high",
            "reason": "Synthetic offline fixture; not an availability assertion",
        }
    return {
        "schema_version": 1,
        "client": "codex",
        "client_version": "synthetic-fixture",
        "auth_mode": "chatgpt",
        "format": fmt,
        "observed_at": "2026-09-14",
        "availability_evidence": "Synthetic catalog, no model API calls",
        "cost_basis": "Synthetic relative cost; no measured economic claim",
        "models": {
            "gpt-fixture-economy": {
                "efforts": ["low", "medium"],
                "modalities": ["text"],
            },
            "gpt-fixture-capable": {
                "efforts": ["medium", "high"],
                "modalities": ["text", "image"],
            },
        },
        "roles": roles,
    }


def snapshot(root, recovery=False):
    return {
        p.relative_to(root).as_posix(): p.read_bytes()
        for p in root.rglob("*")
        if p.is_file() and (recovery or "model-routing-backups" not in p.parts)
    }


class InstallationTests(unittest.TestCase):
    def test_extended_roles_preserve_legacy_bindings_and_roll_back(self):
        for fmt in ("standalone", "registered"):
            with self.subTest(fmt=fmt):
                initial = self.install(request(fmt))
                before = snapshot(self.root)
                prior_roles = kit.inspection(self.root)["roles"]
                req = request(fmt)
                for name in (
                    "wdk_worker_light",
                    "wdk_architect",
                    "wdk_architect_deep",
                    "wdk_reviewer_light",
                    "wdk_reviewer_deep",
                ):
                    req["roles"][name] = copy.deepcopy(req["roles"]["wdk_reviewer"])
                result = self.install(req)
                observed = kit.inspection(self.root)
                self.assertEqual(set(observed["roles"]), set(req["roles"]))
                for name, path in kit.role_paths(fmt).items():
                    self.assertEqual(before[path], snapshot(self.root)[path])
                    self.assertEqual(
                        prior_roles[name]["role_fingerprint"],
                        observed["roles"][name]["role_fingerprint"],
                    )
                for name in set(req["roles"]) - set(kit.ROLES):
                    role = tomllib.loads(
                        (self.root / observed["roles"][name]["path"]).read_text()
                    )
                    if name != "wdk_worker_light":
                        self.assertEqual(role["sandbox_mode"], "read-only")
                self.assertEqual(self.install(req)["status"], "unchanged")
                self.assertBlocked(request(fmt))  # No implicit removal of roles.
                kit.rollback(self.root, result["transaction"])
                self.assertEqual(snapshot(self.root), before)
                kit.rollback(self.root, initial["transaction"])

    def test_extended_role_cannot_adopt_unowned_file(self):
        self.install()
        req = request()
        req["roles"]["wdk_architect"] = copy.deepcopy(req["roles"]["wdk_reviewer"])
        self.put(".codex/agents/wdk_architect.toml", "# user-owned\n")
        self.assertBlocked(req)

    def test_unknown_role_and_invented_effort_rejected(self):
        req = request()
        req["roles"]["wdk_unknown"] = copy.deepcopy(req["roles"]["wdk_worker"])
        self.assertBlocked(req)
        req = request()
        req["models"]["gpt-fixture-economy"]["efforts"].append("light")
        req["roles"]["wdk_worker"]["effort"] = "light"
        self.assertBlocked(req)

    @unittest.skipUnless(os.name == "nt", "Windows junction regression")
    def test_junction_parent_and_root_rejected_without_writes(self):
        outside = Path(self.temp.name) / "outside"
        outside.mkdir()
        marker = outside / "keep.txt"
        marker.write_text("unchanged")
        junction = self.root / ".codex"
        subprocess.run(
            [
                "powershell.exe",
                "-NoProfile",
                "-NonInteractive",
                "-Command",
                "New-Item -ItemType Junction -Path $env:WDK_TEST_LINK "
                "-Target $env:WDK_TEST_TARGET | Out-Null",
            ],
            env={
                **os.environ,
                "WDK_TEST_LINK": str(junction),
                "WDK_TEST_TARGET": str(outside),
            },
            check=True,
            capture_output=True,
            timeout=30,
        )
        self.addCleanup(junction.rmdir)
        with self.assertRaises(ValueError):
            kit.plan(self.root, request())
        with self.assertRaises(ValueError):
            kit.inspection(junction)
        self.assertEqual(marker.read_text(), "unchanged")
        self.assertEqual([p.name for p in outside.iterdir()], ["keep.txt"])

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / "host"
        self.root.mkdir()
        self.put(".agents/AGENTS.md", "Fixture policy")
        self.put(".agents/adapters/codex.md", "Fixture adapter")

    def put(self, path, data):
        target = self.root / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data if isinstance(data, bytes) else data.encode())
        return target

    def install(self, req=None):
        req = req or request()
        return kit.apply(self.root, kit.plan(self.root, req))

    def assertBlocked(self, req):
        before = snapshot(self.root, recovery=True)
        with self.assertRaises((ValueError, TypeError)):
            kit.plan(self.root, req)
        self.assertEqual(before, snapshot(self.root, recovery=True))

    def test_documented_request_runs_dryrun_apply_inspect(self):
        guide = (
            ROOT
            / "skills/project-onboarding-adapter/references/codex-model-bootstrap.md"
        ).read_text()
        blocks = re.findall(r"```json\n(.*?)\n```", guide, re.S)
        self.assertEqual(len(blocks), 2)
        replacements = {
            "REPLACE_WITH_AVAILABLE_GPT_ECONOMY_ID": "gpt-fixture-economy",
            "REPLACE_WITH_AVAILABLE_GPT_CAPABLE_ID": "gpt-fixture-capable",
            "REPLACE_WITH_AVAILABLE_GPT_STANDARD_ID": "gpt-fixture-standard",
            "REPLACE_WITH_AVAILABLE_GPT_ARCHITECT_ID": "gpt-fixture-architect",
            "CONFIRMED_CLIENT_VERSION": "synthetic-fixture",
            "CONFIRMED_OBSERVATION_DATE": "2026-09-14",
            "CONFIRMED_CLIENT_CATALOG_SOURCE": "synthetic offline catalog",
            "CONFIRMED_COST_UNITS_SOURCE_DATE_AND_TASK_FIT": "synthetic cost, no claim",
            "CONFIRMED_INSTALLED_SCHEMA_AND_VERSION": "synthetic schema evidence",
        }
        example = blocks[0]
        activation = blocks[1]
        for key, value in replacements.items():
            example = example.replace(key, value)
            activation = activation.replace(key, value)
        req = json.loads(example)
        req.update(json.loads("{" + activation + "}"))
        self.put(
            ".codex/config.toml",
            '# preserved\nmodel = "keep-primary"\n[agents]\nenabled = false\n',
        )
        request_path = self.put("request.json", json.dumps(req))
        command = [
            sys.executable,
            str(HELPER),
            "--root",
            str(self.root),
            "--request",
            str(request_path),
        ]
        before = snapshot(self.root, recovery=True)
        preview = subprocess.run(command, capture_output=True, text=True)
        self.assertEqual(preview.returncode, 0, preview.stderr)
        self.assertEqual(
            json.loads(preview.stdout)["review"]["activation"]["before"], False
        )
        self.assertEqual(before, snapshot(self.root, recovery=True))
        applied = subprocess.run(
            [*command, "--apply", "--approve"], capture_output=True, text=True
        )
        self.assertEqual(applied.returncode, 0, applied.stderr)
        inspected = subprocess.run(
            [sys.executable, str(HELPER), "--root", str(self.root), "--inspect"],
            capture_output=True,
            text=True,
        )
        self.assertEqual(inspected.returncode, 0, inspected.stderr)
        report = json.loads(inspected.stdout)
        self.assertEqual(report["activation"], "unverified")
        self.assertEqual(report["native_gate"], "enabled-in-project-config")
        for name, binding in req["roles"].items():
            self.assertEqual(report["roles"][name]["model"], binding["model"])
            self.assertEqual(report["roles"][name]["effort"], binding["effort"])
        parsed = tomllib.loads((self.root / ".codex/config.toml").read_text())
        self.assertEqual(parsed["model"], "keep-primary")
        self.assertTrue(parsed["agents"]["enabled"])

    def test_plan_has_zero_writes(self):
        before = snapshot(self.root, recovery=True)
        self.assertEqual(len(kit.plan(self.root, request())), 5)
        self.assertEqual(before, snapshot(self.root, recovery=True))
        self.assertFalse((self.root / ".codex").exists())
        self.assertFalse((self.root / ".agents/project").exists())

    def test_standalone_install_and_same_input_noop(self):
        result = self.install()
        self.assertEqual(result["status"], "configured")
        self.assertEqual(result["activation"], "unverified")
        self.assertFalse((self.root / kit.CONFIG).exists())
        for role, path in kit.role_paths("standalone").items():
            data = tomllib.loads((self.root / path).read_text())
            self.assertEqual(data["name"], role)
            self.assertEqual(data["model"], request()["roles"][role]["model"])
            self.assertIn(
                "Do not change agent configuration", data["developer_instructions"]
            )
            self.assertNotIn("approval_policy", data)
            if role in {"wdk_lookup", "wdk_reviewer"}:
                self.assertEqual(data["sandbox_mode"], "read-only")
            else:
                self.assertNotIn("sandbox_mode", data)
        before = snapshot(self.root, recovery=True)
        self.assertEqual(self.install()["status"], "unchanged")
        self.assertEqual(before, snapshot(self.root, recovery=True))

    def test_existing_primary_provider_mcp_security_and_global_preserved(self):
        original = b'# user comment\r\nmodel="my-primary"\r\n[agents]\r\nmax_threads=1\r\n[mcp_servers.local]\r\ncommand="tool"\r\n[profiles.safe]\r\nsandbox_mode="read-only"\r\n'
        self.put(kit.CONFIG, original)
        global_config = Path(self.temp.name) / "global-config.toml"
        global_config.write_text('model="global-primary"\n')
        self.install()
        self.assertEqual((self.root / kit.CONFIG).read_bytes(), original)
        self.assertEqual(global_config.read_text(), 'model="global-primary"\n')

    def test_registered_merge_preserves_comments_values_crlf(self):
        original = b'# keep\r\nmodel="user-primary"\r\n[agents.custom]\r\ndescription="Mine"\r\n[profiles.safe]\r\nsandbox_mode="read-only"\r\n'
        self.put(kit.CONFIG, original)
        result = self.install(request("registered"))
        current = (self.root / kit.CONFIG).read_bytes()
        self.assertTrue(current.startswith(original))
        self.assertNotIn(b"\n", current.replace(b"\r\n", b""))
        data = tomllib.loads(current.decode())
        self.assertEqual(data["model"], "user-primary")
        self.assertEqual(data["agents"]["custom"]["description"], "Mine")
        for role, path in kit.role_paths("registered").items():
            self.assertEqual(
                data["agents"][role]["config_file"], path.removeprefix(".codex/")
            )
            layer = tomllib.loads((self.root / path).read_text())
            self.assertNotIn("name", layer)
            self.assertNotIn("description", layer)
        self.assertFalse((self.root / ".codex/agents").exists())
        before = snapshot(self.root, recovery=True)
        self.assertEqual(self.install(request("registered"))["status"], "unchanged")
        self.assertEqual(before, snapshot(self.root, recovery=True))
        self.assertEqual(
            kit.rollback(self.root, result["transaction"])["status"], "rolled-back"
        )
        self.assertEqual((self.root / kit.CONFIG).read_bytes(), original)

    def test_registered_empty_config_and_missing_final_newline(self):
        for content in (b"", b'# comment\nmodel="primary"'):
            with self.subTest(content=content):
                self.put(kit.CONFIG, content)
                result = self.install(request("registered"))
                self.assertEqual(
                    self.install(request("registered"))["status"], "unchanged"
                )
                kit.rollback(self.root, result["transaction"])
                self.assertEqual((self.root / kit.CONFIG).read_bytes(), content)

    def test_validated_binding_update(self):
        self.install()
        before = kit.inspection(self.root)["roles"]
        req = request()
        req["roles"]["wdk_lookup"]["effort"] = "medium"
        result = self.install(req)
        self.assertEqual(
            set(result["changed"]),
            {kit.STATE, kit.role_paths("standalone")["wdk_lookup"]},
        )
        self.assertEqual(result["activation"], "unverified")
        after = kit.inspection(self.root)["roles"]
        self.assertNotEqual(
            before["wdk_lookup"]["role_fingerprint"],
            after["wdk_lookup"]["role_fingerprint"],
        )
        for name in set(kit.ROLES) - {"wdk_lookup"}:
            self.assertEqual(
                before[name]["role_fingerprint"], after[name]["role_fingerprint"]
            )

    def test_unrelated_user_config_edit_survives_role_update(self):
        self.install(request("registered"))
        path = self.root / kit.CONFIG
        path.write_bytes(b'model="new-user-choice"\n' + path.read_bytes())
        req = request("registered")
        req["roles"]["wdk_worker"]["effort"] = "medium"
        self.install(req)
        self.assertEqual(tomllib.loads(path.read_text())["model"], "new-user-choice")

    def test_wrong_client_auth_schema_format(self):
        for key, value in (
            ("client", "cursor"),
            ("client", "claude-code"),
            ("auth_mode", "unknown"),
            ("schema_version", 2),
            ("format", "guess"),
        ):
            with self.subTest(key=key, value=value):
                req = request()
                req[key] = value
                self.assertBlocked(req)

    def test_missing_or_extra_fields_and_empty_evidence(self):
        for key in request():
            req = request()
            del req[key]
            self.assertBlocked(req)
        req = request()
        req["api_key"] = "must-not-be-accepted"
        self.assertBlocked(req)
        for key in (
            "availability_evidence",
            "client_version",
            "cost_basis",
            "observed_at",
        ):
            req = request()
            req[key] = ""
            self.assertBlocked(req)

    def test_missing_model_effort_non_gpt_and_modality(self):
        for mutation in ("model", "effort", "nongpt", "modality", "empty", "roles"):
            with self.subTest(mutation=mutation):
                req = request()
                if mutation == "model":
                    req["roles"]["wdk_lookup"]["model"] = "gpt-not-in-catalog"
                elif mutation == "effort":
                    req["roles"]["wdk_lookup"]["effort"] = "unsupported"
                elif mutation == "nongpt":
                    req["models"]["not-gpt"] = copy.deepcopy(
                        next(iter(req["models"].values()))
                    )
                elif mutation == "modality":
                    req["models"]["gpt-fixture-economy"]["modalities"] = ["image"]
                elif mutation == "empty":
                    req["models"] = {}
                else:
                    del req["roles"]["wdk_reviewer"]
                self.assertBlocked(req)

    def test_disabled_and_invalid_config(self):
        for config in (
            "[agents]\nenabled=false\n",
            "[agents]\nbad = [",
            'agents="invalid"\n',
        ):
            with self.subTest(config=config):
                self.put(kit.CONFIG, config)
                self.assertBlocked(request())

    def test_unowned_role_even_identical_is_not_adopted(self):
        role = "wdk_worker"
        self.put(
            kit.role_paths("standalone")[role],
            kit.render_role(role, request()["roles"][role], "standalone"),
        )
        self.assertBlocked(request())

    def test_collision_name_inside_different_filename(self):
        self.put(".codex/agents/personal.toml", 'name="wdk_worker"\n')
        self.assertBlocked(request())
        self.assertBlocked(request("registered"))

    def test_collision_registration_and_reserved_state(self):
        self.put(kit.CONFIG, '[agents.wdk_lookup]\ndescription="user-owned"\n')
        self.assertBlocked(request())
        (self.root / kit.CONFIG).unlink()
        self.put(kit.STATE, "{}")
        self.assertBlocked(request())

    def test_user_drift_in_owned_file(self):
        self.install()
        self.put(kit.role_paths("standalone")["wdk_worker"], "# user changed this\n")
        self.assertBlocked(request())

    def test_managed_block_drift_and_duplicates(self):
        self.install(request("registered"))
        path = self.root / kit.CONFIG
        data = path.read_text()
        path.write_text(data.replace("description = ", "# comment\ndescription = ", 1))
        self.assertBlocked(request("registered"))
        path.write_text(data + data)
        self.assertBlocked(request("registered"))

    def test_format_switch_requires_migration(self):
        self.install()
        self.assertBlocked(request("registered"))

    def test_no_installed_codex_bundle(self):
        (self.root / ".agents/adapters/codex.md").unlink()
        self.assertBlocked(request())

    def test_symlink_target_refused(self):
        outside = Path(self.temp.name) / "outside"
        outside.mkdir()
        try:
            (self.root / ".codex").symlink_to(outside, target_is_directory=True)
        except OSError as exc:
            if getattr(exc, "winerror", None) == 1314:
                self.skipTest(
                    "Host denies symlink creation; junction coverage runs separately"
                )
            raise
        self.assertBlocked(request())
        self.assertEqual(list(outside.iterdir()), [])
        (self.root / ".codex").unlink()

    def test_hardlink_target_refused(self):
        original = self.put("original", "# source")
        target = self.root / kit.CONFIG
        target.parent.mkdir()
        target.hardlink_to(original)
        self.assertBlocked(request())

    def test_state_path_injection(self):
        self.install()
        path = self.root / kit.STATE
        state = json.loads(path.read_text())
        state["files"]["../../outside"] = "bad"
        path.write_text(json.dumps(state))
        self.assertBlocked(request())

    def test_concurrent_change_before_apply_is_preserved(self):
        changes = kit.plan(self.root, request())
        target = next(iter(changes))
        self.put(target, "# external edit")
        with self.assertRaises(ValueError):
            kit.apply(self.root, changes)
        self.assertEqual((self.root / target).read_text(), "# external edit")
        self.assertFalse((self.root / ".agents/project/.model-routing.lock").exists())

    def test_mid_write_failure_rolls_back_before_and_after_write(self):
        for after in (False, True):
            with self.subTest(after=after):
                before = snapshot(self.root)
                calls = []

                def failing_writer(root, path, data):
                    calls.append(path)
                    if len(calls) == 3 and not after:
                        raise OSError("injected before write")
                    kit.atomic_write(root, path, data)
                    if len(calls) == 3:
                        raise OSError("injected after write")

                with self.assertRaises(OSError):
                    kit.apply(
                        self.root, kit.plan(self.root, request()), writer=failing_writer
                    )
                self.assertEqual(before, snapshot(self.root))
                self.assertFalse(
                    (self.root / ".agents/project/.model-routing.lock").exists()
                )

    def test_rollback_idempotent_and_backups_restricted(self):
        before = snapshot(self.root)
        result = self.install()
        journal = self.root / kit.BACKUPS / result["transaction"] / "journal.json"
        if os.name == "nt":
            # Read the real resulting FILE ACL, not chmod bits or the helper's report.
            script = r"""
$ErrorActionPreference = 'Stop'
$a = Get-Acl -LiteralPath $env:WDK_TEST_JOURNAL
$r = @($a.GetAccessRules($true, $true,
    [System.Security.Principal.SecurityIdentifier]))
@{ identities = @($r | ForEach-Object { $_.IdentityReference.Value });
   current = [System.Security.Principal.WindowsIdentity]::GetCurrent().User.Value;
   rights = @($r | ForEach-Object { $_.FileSystemRights.ToString() });
   types = @($r | ForEach-Object { $_.AccessControlType.ToString() })
} | ConvertTo-Json -Compress
"""
            shell = (
                Path(os.environ["SystemRoot"])
                / "System32/WindowsPowerShell/v1.0/powershell.exe"
            )
            acl_result = subprocess.run(
                [str(shell), "-NoProfile", "-NonInteractive", "-Command", script],
                env={
                    **{
                        k: v
                        for k, v in os.environ.items()
                        if k.lower() != "psmodulepath"
                    },
                    "PSModulePath": str(shell.parent / "Modules"),
                    "WDK_TEST_JOURNAL": str(journal),
                },
                check=True,
                capture_output=True,
                text=True,
                timeout=30,
            )
            acl = json.loads(acl_result.stdout)
            self.assertEqual(acl["identities"], [acl["current"]])
            self.assertEqual(acl["rights"], ["FullControl"])
            self.assertEqual(acl["types"], ["Allow"])
        else:
            self.assertEqual(journal.stat().st_mode & 0o777, 0o600)
            self.assertEqual(journal.parent.stat().st_mode & 0o777, 0o700)
        kit.rollback(self.root, result["transaction"])
        self.assertEqual(before, snapshot(self.root))
        self.assertEqual(
            kit.rollback(self.root, result["transaction"])["status"], "unchanged"
        )

    def test_journal_protection_failure_blocks_before_sensitive_writes(self):
        self.put(kit.CONFIG, 'model = "existing-primary"\n# sensitive config fixture\n')
        before = snapshot(self.root, recovery=True)
        with patch.object(
            kit, "protect_journal_directory", side_effect=ValueError("ACL denied")
        ):
            with self.assertRaises(ValueError):
                self.install(request("registered"))
        self.assertEqual(snapshot(self.root, recovery=True), before)
        self.assertFalse((self.root / ".agents/project/.model-routing.lock").exists())

    def test_rollback_preserves_later_user_edits(self):
        result = self.install(request("registered"))
        path = self.root / kit.CONFIG
        path.write_text("# new user comment\n" + path.read_text())
        before = snapshot(self.root, recovery=True)
        with self.assertRaises(ValueError):
            kit.rollback(self.root, result["transaction"])
        self.assertEqual(before, snapshot(self.root, recovery=True))

    def test_rollback_rejects_path_injection(self):
        result = self.install()
        journal = self.root / kit.BACKUPS / result["transaction"] / "journal.json"
        journal.write_text(
            json.dumps({"../../outside": {"before": None, "after": None}})
        )
        with self.assertRaises(ValueError):
            kit.rollback(self.root, result["transaction"])
        with self.assertRaises(ValueError):
            kit.rollback(self.root, "../../outside")

    def test_lock_prevents_another_installer(self):
        self.put(".agents/project/.model-routing.lock", "")
        before = snapshot(self.root, recovery=True)
        with self.assertRaises(FileExistsError):
            self.install()
        self.assertEqual(before, snapshot(self.root, recovery=True))

    def test_cli_dry_run_approval_and_configuration_status(self):
        req = self.put(
            ".agents/project/model-routing-request.json", json.dumps(request())
        )
        command = [
            sys.executable,
            str(HELPER),
            "--root",
            str(self.root),
            "--request",
            str(req),
        ]
        before = snapshot(self.root, recovery=True)
        dry = subprocess.run(command, capture_output=True, text=True)
        self.assertEqual(dry.returncode, 0, dry.stderr)
        self.assertEqual(json.loads(dry.stdout)["status"], "proposed")
        self.assertEqual(before, snapshot(self.root, recovery=True))
        denied = subprocess.run([*command, "--apply"], capture_output=True, text=True)
        self.assertNotEqual(denied.returncode, 0)
        self.assertEqual(before, snapshot(self.root, recovery=True))
        applied = subprocess.run(
            [*command, "--apply", "--approve"], capture_output=True, text=True
        )
        self.assertEqual(applied.returncode, 0, applied.stderr)
        self.assertEqual(json.loads(applied.stdout)["activation"], "unverified")

    def activation_request(self, key="agents.enabled", fmt="standalone"):
        req = request(fmt)
        req["activation"] = {
            "config_key": key,
            "schema_evidence": "Synthetic installed-schema fixture; not runtime proof",
            "allow_enable": True,
        }
        return req

    def test_legacy_disabled_gate_is_not_silently_ignored(self):
        self.put(kit.CONFIG, "[features]\nmulti_agent = false\n")
        self.assertBlocked(request())

    def test_approved_gate_enabling_preserves_other_config_and_rolls_back(self):
        for key in ("agents.enabled", "features.multi_agent"):
            for fmt in ("standalone", "registered"):
                with self.subTest(key=key, fmt=fmt):
                    section, field = key.split(".")
                    original = (
                        '# keep\r\nmodel = "primary"\r\n'
                        f"[{section}] # settings\r\n{field} = false # deliberate\r\n"
                        '[mcp_servers.local]\r\ncommand = "tool"\r\n'
                    ).encode()
                    self.put(kit.CONFIG, original)
                    before = snapshot(self.root)
                    req = self.activation_request(key, fmt)
                    changes = kit.plan(self.root, req)
                    self.assertEqual(before, snapshot(self.root))
                    result = kit.apply(self.root, changes)
                    data = tomllib.loads((self.root / kit.CONFIG).read_text())
                    self.assertIs(data[section][field], True)
                    self.assertEqual(data["model"], "primary")
                    self.assertEqual(data["mcp_servers"]["local"]["command"], "tool")
                    self.assertIn(
                        b"true # deliberate\r\n", (self.root / kit.CONFIG).read_bytes()
                    )
                    self.assertEqual(self.install(req)["status"], "unchanged")
                    self.assertEqual(result["activation"], "unverified")
                    kit.rollback(self.root, result["transaction"])
                    self.assertEqual(before, snapshot(self.root))

    def test_activation_missing_gate_existing_table_and_dotted_key(self):
        for original in (
            "",
            "[agents]\nmax_threads = 2\n",
            '[agents.user_role]\ndescription = "mine"\n',
            'agents.enabled = false # keep\nmodel = "primary"\n',
        ):
            with self.subTest(original=original):
                self.put(kit.CONFIG, original)
                before = snapshot(self.root)
                result = self.install(self.activation_request())
                data = tomllib.loads((self.root / kit.CONFIG).read_text())
                self.assertIs(data["agents"]["enabled"], True)
                kit.rollback(self.root, result["transaction"])
                self.assertEqual(before, snapshot(self.root))

    def test_activation_cannot_mask_other_disabled_gate(self):
        self.put(
            kit.CONFIG, "[agents]\nenabled = false\n[features]\nmulti_agent = false\n"
        )
        self.assertBlocked(self.activation_request())
        self.assertBlocked(self.activation_request("features.multi_agent"))

    def test_invalid_activation_scope_and_missing_consent_rejected(self):
        for field, value in (
            ("config_key", "sandbox_mode"),
            ("config_key", "projects.trust_level"),
            ("schema_evidence", ""),
            ("allow_enable", False),
            ("allow_enable", "yes"),
        ):
            req = self.activation_request()
            req["activation"][field] = value
            self.assertBlocked(req)
        req = self.activation_request()
        req["activation"]["global"] = True
        self.assertBlocked(req)

    def test_activation_does_not_rewrite_multiline_lookalike(self):
        original = 'developer_instructions = """\n[agents]\nenabled = false\n"""\n[agents]\nenabled = false\n'
        self.put(kit.CONFIG, original)
        self.install(self.activation_request())
        data = tomllib.loads((self.root / kit.CONFIG).read_text())
        self.assertEqual(
            data["developer_instructions"],
            tomllib.loads(original)["developer_instructions"],
        )
        self.assertIs(data["agents"]["enabled"], True)

    def test_activation_inline_table_refuses_unsafe_rewrite(self):
        self.put(kit.CONFIG, "agents = { enabled = false, max_threads = 1 }\n")
        self.assertBlocked(self.activation_request())

    def test_existing_v1_state_can_add_activation_and_preserve_it(self):
        self.install()
        self.install(self.activation_request())
        self.assertIs(
            tomllib.loads((self.root / kit.CONFIG).read_text())["agents"]["enabled"],
            True,
        )
        req = request()
        req["roles"]["wdk_worker"]["effort"] = "medium"
        self.install(req)
        state = json.loads((self.root / kit.STATE).read_text())
        self.assertEqual(state["activation"]["config_key"], "agents.enabled")
        self.assertEqual(self.install(req)["status"], "unchanged")

    def test_activation_user_drift_is_not_silently_reenabled(self):
        self.install(self.activation_request())
        self.put(kit.CONFIG, "[agents]\nenabled = false\n")
        self.assertBlocked(self.activation_request())

    def test_inspect_is_readonly_and_never_claims_runtime_activation(self):
        self.install(self.activation_request())
        command = [sys.executable, str(HELPER), "--root", str(self.root), "--inspect"]
        before = snapshot(self.root, recovery=True)
        result = subprocess.run(command, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        data = json.loads(result.stdout)
        self.assertEqual(data["activation"], "unverified")
        self.assertEqual(data["native_gate"], "enabled-in-project-config")
        self.assertEqual(len(data["configuration_fingerprint"]), 64)
        self.assertEqual(set(data["roles"]), set(kit.ROLES))
        self.assertEqual(before, snapshot(self.root, recovery=True))
        self.put(kit.CONFIG, "# unrelated drift\n[agents]\nenabled = true\n")
        changed = json.loads(
            subprocess.run(command, capture_output=True, text=True).stdout
        )
        self.assertNotEqual(
            data["configuration_fingerprint"], changed["configuration_fingerprint"]
        )

    def test_dry_run_includes_narrow_review_not_unrelated_secrets(self):
        self.put(kit.CONFIG, 'model="primary"\nprivate_value="DO_NOT_PRINT"\n')
        req = self.put(
            ".agents/project/request.json", json.dumps(self.activation_request())
        )
        command = [
            sys.executable,
            str(HELPER),
            "--root",
            str(self.root),
            "--request",
            str(req),
        ]
        result = subprocess.run(command, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        data = json.loads(result.stdout)
        self.assertIs(data["review"]["activation"]["after"], True)
        self.assertEqual(
            data["review"]["roles"]["wdk_worker"]["model"], "gpt-fixture-economy"
        )
        self.assertNotIn("DO_NOT_PRINT", result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main()
