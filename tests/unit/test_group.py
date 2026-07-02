import uuid

from xkoranate.group import XkorGroup


def test_defaults():
    g = XkorGroup()
    assert g.name == ""
    assert g.athletes == []


def test_constructor_sets_fields():
    ids = [uuid.uuid4(), uuid.uuid4()]
    g = XkorGroup("Group A", ids)
    assert g.name == "Group A"
    assert g.athletes == ids


def test_clone_is_independent_copy():
    ids = [uuid.uuid4()]
    g = XkorGroup("Group A", ids)
    clone = g.clone()

    assert clone is not g
    assert clone.name == g.name
    assert clone.athletes == g.athletes

    clone.athletes.append(uuid.uuid4())
    assert len(g.athletes) == 1
