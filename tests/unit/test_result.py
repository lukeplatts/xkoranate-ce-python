import uuid

from xkoranate.athlete import XkorAthlete
from xkoranate.result import XkorResult


def test_defaults():
    r = XkorResult()
    assert r.score() == 0.0
    assert r.output() == ""
    assert r.contains("score") is False


def test_constructor_sets_score():
    r = XkorResult(score=12.5)
    assert r.score() == 12.5
    assert r.contains("score") is True


def test_constructor_sets_score_string():
    r = XkorResult(scoreString="12.50s")
    assert r.scoreString() == "12.50s"


def test_scoreString_falls_back_to_formatted_score():
    r = XkorResult(score=1.0)
    assert r.scoreString() == "1"


def test_setOutput_and_output():
    r = XkorResult()
    r.setOutput("some text")
    assert r.output() == "some text"


def test_clone_copies_athlete_and_result_dict():
    a = XkorAthlete(uuid.uuid4())
    r = XkorResult(score=3.0, ath=a)
    r.setOutput("line")

    clone = r.clone()

    assert clone is not r
    assert clone.athlete is not a
    assert clone.athlete.id == a.id
    assert clone.result == r.result

    clone.setOutput("changed")
    assert r.output() == "line"


def test_value_returns_raw_result_entry():
    r = XkorResult()
    r.result["custom"] = 42
    assert r.value("custom") == 42
    assert r.value("missing") is None


def test_eq_compares_by_athlete_id():
    u = uuid.uuid4()
    r1 = XkorResult(ath=XkorAthlete(u))
    r2 = XkorResult(ath=XkorAthlete(u))
    r3 = XkorResult(ath=XkorAthlete(uuid.uuid4()))
    assert r1 == r2
    assert r1 != r3
