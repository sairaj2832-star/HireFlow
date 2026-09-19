"""Config loader — validates the 5 B0 YAML configs at startup."""

import hashlib
import json
from pathlib import Path
from typing import Any

import yaml  # type: ignore[import-untyped]

ROOT = Path(__file__).resolve().parents[2]
CONFIGS = Path(__file__).resolve().parents[3] / "configs"


def _load(p: Path) -> dict[str, Any]:
    return dict(yaml.safe_load(p.read_text(encoding="utf-8")))


def load_policy() -> dict[str, Any]:
    return _load(ROOT / "policy.yaml")


def load_taxonomy() -> dict[str, Any]:
    return _load(ROOT / "taxonomy_slice.yaml")


def load_registry() -> dict[str, Any]:
    return _load(ROOT / "registry.yaml")


def load_evidence_taxonomy() -> dict[str, Any]:
    return _load(CONFIGS / "evidence_taxonomy.yaml")


def load_consent() -> dict[str, Any]:
    return _load(CONFIGS / "consent.yaml")


def policy_hash() -> str:
    return hashlib.sha256(json.dumps(load_policy(), sort_keys=True).encode()).hexdigest()[:16]
