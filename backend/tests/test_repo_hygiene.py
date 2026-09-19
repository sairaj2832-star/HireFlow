# backend/tests/test_repo_hygiene.py
from pathlib import Path


def test_repo_scaffold_exists():
    root = Path(__file__).resolve().parents[2]
    assert (root / "backend" / "app" / "models").exists()
    assert (root / "backend" / "artifacts").exists()
    assert (root / "frontend" / "src").exists()
    assert (root / "configs").exists()
    assert (root / ".gitignore").exists()


def test_gitignore_covers_secrets_and_db():
    root = Path(__file__).resolve().parents[2]
    text = (root / ".gitignore").read_text()
    assert ".venv" in text
    assert "hireflow.db" in text
    assert ".env" in text
    assert "artifacts/journal.jsonl" in text
    assert "node_modules" in text
