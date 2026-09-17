"""Tests use temporary profiles only; never mutate the live fleet."""
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

SCRIPT = Path(__file__).with_name("fleet-inventory.py")
spec = importlib.util.spec_from_file_location("inventory", SCRIPT)
inventory = importlib.util.module_from_spec(spec)
spec.loader.exec_module(inventory)


class InventoryTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.home = Path(self.temp.name)
        self.profile = self.home / "profiles/test-bot"
        self.profile.mkdir(parents=True)
        self.write("config.yaml", "model:\n  default: auto\n  provider: nous\nagent:\n  reasoning_effort: medium\n")

    def write(self, name, value):
        path = self.profile / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(value, encoding="utf-8")

    def row(self):
        return inventory.collect(self.home)["profiles"][0]

    def test_valid_inventory_is_not_runtime_proof(self):
        self.write("auth.json", "DO_NOT_READ_AUTH_TOKEN")
        self.write(".env", "export API_KEY=DO_NOT_PRINT_ENV\nINVALID-NAME=ignore\n# COMMENT=x\n")
        self.write("cron/jobs.json", json.dumps({"jobs": [{"enabled": True, "prompt": "DO_NOT_PRINT_PROMPT"}]}))
        row = self.row()
        self.assertEqual(row["errors"], [])
        self.assertEqual(row["env_var_names"], ["API_KEY"])
        self.assertEqual(row["cron_stored_job_count"], 1)
        self.assertEqual(row["runtime_readiness"], "not_checked")
        self.assertTrue(row["auth_json_exists"])
        self.assertNotIn("DO_NOT_", json.dumps(row))

    def test_invalid_yaml_redacts_parser_source(self):
        self.write("config.yaml", "secret: [DO_NOT_PRINT_SECRET\n")
        row = self.row()
        self.assertIn("config:invalid_yaml", row["errors"])
        self.assertNotIn("DO_NOT_PRINT_SECRET", json.dumps(row))

    def test_bad_config_shapes(self):
        for config in ["[]", "null", "42"]:
            with self.subTest(config=config):
                self.write("config.yaml", config)
                self.assertIn("config:invalid_shape", self.row()["errors"])
        self.write("config.yaml", "model: hello\nagent: []\nweb: false\nproviders: null")
        self.assertEqual(len(self.row()["errors"]), 4)

    def test_dependency_missing_explicit(self):
        with patch.object(inventory, "yaml", None):
            self.assertIn("config:dependency_missing", self.row()["errors"])

    def test_unreadable_yaml_does_not_crash(self):
        with patch.object(Path, "read_text", side_effect=PermissionError("DO_NOT_PRINT")):
            self.assertEqual(inventory.load_yaml(self.profile / "config.yaml"), ({}, "unreadable"))

    def test_missing_config_and_home(self):
        (self.profile / "config.yaml").unlink()
        self.assertIn("config:missing", self.row()["errors"])
        self.assertEqual(inventory.collect(self.home / "absent")["errors"], ["profiles_directory_missing"])

    def test_malformed_cron_is_unknown_not_zero(self):
        for content in ["{bad", '{"jobs":{}}', '[1]', '{}']:
            with self.subTest(content=content):
                self.write("cron/jobs.json", content)
                row = self.row()
                self.assertIsNone(row["cron_stored_job_count"])
                self.assertIn("cron:invalid_or_unreadable", row["errors"])

    def test_list_cron_and_yaml_not_registration(self):
        self.write("cron/jobs.json", '[{"enabled":true},{"enabled":false}]')
        self.write("cron/z.yaml", "enabled: true")
        self.write("cron/a.yaml", "enabled: true")
        row = self.row()
        self.assertEqual(row["cron_stored_job_count"], 2)
        self.assertEqual(row["cron_explicitly_enabled_count"], 1)
        self.assertEqual(row["cron_yaml_files_not_registration_evidence"], ["a.yaml", "z.yaml"])

    def test_bom_and_scalar_type(self):
        self.write("config.yaml", '\ufeffmodel:\n  default: [bad]\n')
        self.assertIn("config:default:invalid_type", self.row()["errors"])

    def test_deterministic_and_read_only(self):
        (self.home / "profiles/.deleted").mkdir()
        before = {str(p): p.read_bytes() for p in self.home.rglob("*") if p.is_file()}
        a = json.dumps(inventory.collect(self.home), sort_keys=True)
        b = json.dumps(inventory.collect(self.home), sort_keys=True)
        self.assertEqual(a, b)
        self.assertEqual(inventory.collect(self.home)["profile_count"], 1)
        self.assertEqual(before, {str(p): p.read_bytes() for p in self.home.rglob("*") if p.is_file()})

    def test_cli_bad_profile_exit_nonzero(self):
        import os
        self.write("config.yaml", "[]")
        run = subprocess.run([sys.executable, str(SCRIPT)], env=dict(os.environ, HERMES_AUDIT_HOME=str(self.home)), capture_output=True)
        self.assertEqual(run.returncode, 1)
        self.assertIn("config:invalid_shape", run.stdout.decode())


if __name__ == "__main__":
    unittest.main()
