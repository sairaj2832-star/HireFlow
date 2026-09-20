# backend/tests/conftest.py — repo-wide offline guarantee (AGENTS.md §9)
# Nulls the classifier-relevant API keys for EVERY test so make_classifier()
# short-circuits to the deterministic seeded offline fallback — the suite never
# opens a socket to a live Jev/LLM provider, regardless of backend/.env contents.
# test_jevs.py::test_make_classifier_feature_flag is compatible: it overrides
# settings.typesafe_api_key by plain assignment during its body and make_classifier()
# reads it at call time, so JevClassifier selection still holds; monkeypatch teardown
# restores the original keys afterward.
import pytest


@pytest.fixture(autouse=True)
def _offline_classifier(monkeypatch):
    from app.config import settings

    monkeypatch.setattr(settings, "typesafe_api_key", None)
    monkeypatch.setattr(settings, "gemini_api_key", None)
    monkeypatch.setattr(settings, "openrouter_api_key", None)