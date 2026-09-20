import pytest
from pydantic import ValidationError
from app.models.classifier import Judgement, ScreenQuestion, Classifier, ClassifierUnavailable  # noqa: F401


def test_judgement_valid():
    j = Judgement(p=0.7, confidence=0.9, distribution={"supporting": 0.7, "neutral": 0.3})
    assert j.p == 0.7


def test_judgement_rejects_out_of_range():
    with pytest.raises(ValidationError):
        Judgement(p=1.5, confidence=0.5, distribution={})
    with pytest.raises(ValidationError):
        Judgement(p=0.5, confidence=-0.1, distribution={})


def test_screen_question_shape():
    q = ScreenQuestion(id="cand_01:REQ-01", requirement_id="REQ-01",
                       requirement_text="Python", candidate_text="built APIs in Python",
                       span_quote="built REST APIs using Python")
    assert q.id == "cand_01:REQ-01"


def test_errors_are_runtime_errors():
    assert issubclass(ClassifierUnavailable, RuntimeError)