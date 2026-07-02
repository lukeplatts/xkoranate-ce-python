from xkoranate.rplist import XkorRPList


def test_defaults():
    rp = XkorRPList()
    assert rp.competitionName() == ""
    assert rp.rpCalculationType() == "olympic"
    assert rp.rpEffect() == 15.0
    assert rp.useTeams() is True
    assert rp.useWGStyleBonus() is False


def test_addBonus_and_bonus_lookup():
    rp = XkorRPList()
    rp.addBonus(("AAA", {"bonus": 0.5}))
    assert rp.bonus("AAA") == 0.5


def test_bonus_defaults_to_zero_for_unknown_code():
    rp = XkorRPList()
    assert rp.bonus("ZZZ") == 0.0


def test_bonus_scales_between_min_and_max():
    rp = XkorRPList()
    rp.setMinBonus(0.0)
    rp.setMaxBonus(2.0)
    rp.addBonus(("AAA", {"bonus": 1.0}))
    assert rp.bonus("AAA") == 0.5


def test_useWGStyleBonus_true_only_for_relative_type():
    rp = XkorRPList()
    rp.setRPCalculationType("relative")
    assert rp.useWGStyleBonus() is True
    rp.setRPCalculationType("olympic")
    assert rp.useWGStyleBonus() is False


def test_setters_round_trip():
    rp = XkorRPList()
    rp.setCompetitionName("Test Cup")
    rp.setRPEffect(25.0)
    rp.setUseTeams(False)
    rp.setBonuses({"AAA": {"bonus": 1.0}})
    rp.setRPOptions({"foo": "bar"})

    assert rp.competitionName() == "Test Cup"
    assert rp.rpEffect() == 25.0
    assert rp.useTeams() is False
    assert rp.bonuses() == {"AAA": {"bonus": 1.0}}
    assert rp.rpOptions() == {"foo": "bar"}
