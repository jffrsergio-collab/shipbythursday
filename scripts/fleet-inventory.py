"""Read-only fleet inventory; no inference, network, scheduling or repairs.

Requires PyYAML (already installed); missing dependency is an explicit error.
Output uses allowlisted configuration fields, never raw auth/env/job contents.
Filesystem presence does not establish authentication, delivery or readiness.
No volatile session timestamps: unchanged inspected inputs produce stable JSON.
This is an inventory helper, not a conversational fleet auditor.
"""
from pathlib import Path
import hashlib
import json
import os
import re
import sys

try:
    import yaml
except ImportError:
    yaml = None

HERMES_HOME = Path(os.environ.get("HERMES_AUDIT_HOME", r"C:\Users\jffrs\AppData\Local\hermes"))


def sha(data):
    return hashlib.sha256(data).hexdigest()


def env_var_names(path):
    if not path.exists():
        return []
    names = []
    for line in path.read_text(encoding="utf-8-sig").splitlines():
        match = re.match(r"^\s*(?:export\s+)?([A-Za-z_][A-Za-z0-9_]*)\s*=", line)
        if match:
            names.append(match[1])
    return sorted(set(names))


def load_yaml(path):
    if not path.exists():
        return {}, "missing"
    if yaml is None:
        return {}, "dependency_missing"
    try:
        config = yaml.safe_load(path.read_text(encoding="utf-8-sig"))
    except (OSError, UnicodeError):
        return {}, "unreadable"
    except yaml.YAMLError:
        # Parser exception strings can embed secret source lines.
        return {}, "invalid_yaml"
    if not isinstance(config, dict):
        return {}, "invalid_shape"
    return config, "parsed"


def audit_profile(profile):
    config, status = load_yaml(profile / "config.yaml")
    errors = [] if status == "parsed" else ["config:" + status]

    def block(name):
        value = config.get(name, {})
        if not isinstance(value, dict):
            errors.append("config:" + name + ":invalid_shape")
            return {}
        return value

    def scalar(mapping, key):
        value = mapping.get(key)
        if value is not None and not isinstance(value, str):
            errors.append("config:" + key + ":invalid_type")
            return None
        return value

    model, agent, web = block("model"), block("agent"), block("web")
    provider_block = block("providers")
    jobs_file = profile / "cron/jobs.json"
    jobs_status, job_count, enabled_count = "absent", 0, 0
    if jobs_file.exists():
        try:
            data = json.loads(jobs_file.read_text(encoding="utf-8-sig"))
            jobs = data.get("jobs") if isinstance(data, dict) else data
            if not isinstance(jobs, list) or any(not isinstance(j, dict) for j in jobs):
                raise ValueError("invalid shape")
            jobs_status, job_count = "parsed", len(jobs)
            enabled_count = sum(j.get("enabled") is True for j in jobs)
        except (ValueError, OSError, UnicodeError):
            jobs_status, job_count, enabled_count = "invalid_or_unreadable", None, None
            errors.append("cron:" + jobs_status)
    try:
        names = env_var_names(profile / ".env")
    except (OSError, UnicodeError):
        names = None
        errors.append("env:unreadable")
    try:
        digest = sha((profile / "config.yaml").read_bytes()) if (profile / "config.yaml").exists() else None
    except OSError:
        digest = None
        errors.append("config:hash_unreadable")
    output = {
        "profile": profile.name,
        "config_status": status,
        "config_sha256": digest,
        "model_default": scalar(model, "default"),
        "model_provider": scalar(model, "provider"),
        "reasoning_effort": scalar(agent, "reasoning_effort"),
        "web_backends": {key: scalar(web, key) for key in ("search_backend", "extract_backend")},
        "custom_providers": sorted(str(key) for key in provider_block),
        "env_var_names": names,
        "auth_json_exists": (profile / "auth.json").is_file(),
        "soul_exists": (profile / "SOUL.md").is_file(),
        "memories_md_exists": (profile / "memories.md").is_file(),
        "memory_files": sorted(p.name for p in (profile / "memories").glob("*.md")),
        "cron_storage_status": jobs_status,
        "cron_stored_job_count": job_count,
        "cron_explicitly_enabled_count": enabled_count,
        "cron_yaml_files_not_registration_evidence": sorted(p.name for p in (profile / "cron").glob("*.yaml")),
        "runtime_readiness": "not_checked",
    }
    output["errors"] = sorted(set(errors))
    return output


def collect(home):
    profiles = home / "profiles"
    if not profiles.is_dir():
        return {"errors": ["profiles_directory_missing"], "profiles": [], "profile_count": 0}
    rows = []
    for profile in sorted(p for p in profiles.iterdir() if p.is_dir() and not p.name.startswith(".")):
        try:
            rows.append(audit_profile(profile))
        except OSError:
            rows.append({"profile": profile.name, "errors": ["profile:unreadable"], "runtime_readiness": "not_checked"})
    return {"schema_version": 2, "scope": "profile_files_only; root/shared auth and runtime not tested",
            "profile_count": len(rows), "profiles": rows}


def main():
    report = collect(HERMES_HOME)
    data = (json.dumps(report, indent=2, sort_keys=True, ensure_ascii=False) + "\n").encode("utf-8")
    if "--hash" in sys.argv:
        print(sha(data))
    else:
        sys.stdout.buffer.write(data)
    return int(bool(report.get("errors") or any(p["errors"] for p in report["profiles"])))


if __name__ == "__main__":
    raise SystemExit(main())
