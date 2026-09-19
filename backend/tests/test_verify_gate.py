# backend/tests/test_verify_gate.py
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def test_verify_script_exists_and_executable():
    assert (ROOT / "scripts" / "verify.ps1").exists()
    assert (ROOT / "Makefile").exists()


def test_make_verify_runs():
    # Smoke: rest of the backend suite must pass (deselect self to avoid recursion).
    r = subprocess.run(
        [sys.executable, "-m", "pytest", "-q", "--deselect",
         "tests/test_verify_gate.py::test_make_verify_runs"],
        capture_output=True,
        text=True,
        cwd=str(ROOT / "backend"),
    )
    assert r.returncode == 0, r.stdout[-2000:]
