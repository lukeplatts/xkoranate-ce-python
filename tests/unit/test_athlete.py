import uuid

from xkoranate.athlete import XkorAthlete


def test_defaults():
    a = XkorAthlete()
    assert a.name == ""
    assert a.id is None
    assert a.skill == 0.0
    assert a.nation == ""
    assert a.properties == {}


def test_clone_is_a_deep_copy_of_properties():
    a = XkorAthlete(uuid.uuid4())
    a.name = "Runner"
    a.skill = 0.75
    a.nation = "AAA"
    a.properties["custom"] = "value"

    b = a.clone()

    assert b is not a
    assert b.id == a.id
    assert b.name == a.name
    assert b.skill == a.skill
    assert b.nation == a.nation
    assert b.properties == a.properties

    b.properties["custom"] = "changed"
    assert a.properties["custom"] == "value"


def test_property_getters():
    a = XkorAthlete(uuid.UUID(int=1))
    a.name = "Runner"
    a.nation = "AAA"
    a.skill = 0.5
    a.properties["team"] = "Red"

    assert a.property("name") == "Runner"
    assert a.property("id") == "{%s}" % a.id
    assert a.property("nation") == "AAA"
    assert a.property("skill") == 0.5
    assert a.property("team") == "Red"
    assert a.property("missing") is None


def test_property_getter_id_when_none():
    a = XkorAthlete()
    assert a.property("id") == ""


def test_setProperty_coerces_known_keys():
    a = XkorAthlete()
    a.setProperty("name", 123)
    assert a.name == "123"

    a.setProperty("skill", "0.5")
    assert a.skill == 0.5

    a.setProperty("nation", 7)
    assert a.nation == "7"

    u = uuid.uuid4()
    a.setProperty("id", "{%s}" % u)
    assert a.id == u


def test_setProperty_stores_unknown_keys_in_properties():
    a = XkorAthlete()
    a.setProperty("custom", "value")
    assert a.properties["custom"] == "value"


def test_lt_orders_by_id_int_and_none_first():
    a = XkorAthlete(uuid.UUID(int=1))
    b = XkorAthlete(uuid.UUID(int=2))
    c = XkorAthlete(None)
    assert a < b
    assert not (b < a)
    assert c < a


def test_eq_compares_by_id():
    u = uuid.uuid4()
    a = XkorAthlete(u)
    b = XkorAthlete(u)
    c = XkorAthlete(uuid.uuid4())
    assert a == b
    assert a != c
    assert a != "not an athlete"


def test_hash_uses_id():
    u = uuid.uuid4()
    a = XkorAthlete(u)
    b = XkorAthlete(u)
    assert hash(a) == hash(b)
