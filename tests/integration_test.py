"""End-to-end integration test: app boot, event creation, scorination, save/load."""

import os
import sys
import uuid

import pytest

from xkoranate.application import XkorApplication
from xkoranate.athlete import XkorAthlete
from xkoranate.competitions.competitionfactory import XkorCompetitionFactory
from xkoranate.event import XkorEvent
from xkoranate.group import XkorGroup
from xkoranate.paradigms.paradigmfactory import XkorParadigmFactory
from xkoranate.rng import Mt19937
from xkoranate.rplist import XkorRPList
from xkoranate.signuplist import XkorSignupList
from xkoranate.xml.xmlindex import XkorXmlIndex
from xkoranate.xml.xmlreader import XkorXmlReader
from xkoranate.xml.xmlsportreader import XkorXmlSportReader
from xkoranate.xml.xmlwriter import XkorXmlWriter

NATIONS = ["AAA", "BBB", "CCC", "DDD", "EEE", "FFF", "GGG", "HHH"]

SCORINATE_CASES = [
    ("Athletics—Men’s 00100 m—Round 1", None),
    ("Badminton—xkoranate formula", "matches"),
    ("Association football—SQIS formula", "roundRobin"),
    ("Association football—Footba11er formula", "matches"),
]


@pytest.fixture(scope="module")
def sport_index():
    index = XkorXmlIndex()
    index.traverse("sports:")
    return index


@pytest.fixture(scope="module")
def rng():
    return Mt19937(2026)


def build_event(index, rng, sportName, nAthletes=8):
    sportFile = index.lookup(sportName)
    reader = XkorXmlSportReader(sportFile)
    sport = reader.sport()
    sport.setPRNG(rng)

    sl = XkorSignupList()
    athletes = []
    for i in range(nAthletes):
        a = XkorAthlete()
        a.name = "Athlete %d" % (i + 1)
        a.nation = NATIONS[i % len(NATIONS)]
        a.skill = (i + 1) / float(nAthletes + 1)
        sl.addAthlete(a)
        athletes.append(a)

    ev = XkorEvent()
    ev.setName("Test " + sportName)
    ev.setSignupList(sl)
    ev.setSport(sportName, sport.paradigm())
    ev.addGroup(XkorGroup("Group A", [a.id for a in athletes]))
    return ev, sport


def scorinate(index, rng, sportName, competition=None):
    ev, sport = build_event(index, rng, sportName)
    par = XkorParadigmFactory.newParadigmForSport(sport, {})
    comp = competition or par.defaultCompetition()
    startList = ev.makeStartList(XkorRPList())
    c = XkorCompetitionFactory.newCompetitionFull(
        comp, startList, sport, ev.paradigmOptions(), ev.competitionOptions(), {})
    n = c.matchdays()
    outputs = []
    for md in range(n if n > 0 else 1):
        c.scorinate(md)
        outputs.append(c.results(md))
    return outputs


def test_app_boots_and_loads_sports():
    app = XkorApplication(sys.argv)
    app.loadSports()
    assert app.cw is not None


@pytest.mark.parametrize("sportName,competition", SCORINATE_CASES)
def test_scorinate_produces_results(sport_index, rng, sportName, competition):
    outputs = scorinate(sport_index, rng, sportName, competition)
    assert outputs
    assert outputs[0].strip() != ""


def test_save_load_roundtrip(sport_index, rng, tmp_path):
    ev, sport = build_event(sport_index, rng, "Athletics—Men’s 00100 m—Round 1")
    ev.setCompetition("standard")
    ev.setResult(0, "some result text\nline 2")
    rp = XkorRPList()
    rp.setCompetitionName("Test Cup")
    rp.addBonus(("AAA", {"bonus": 0.5}))

    xmlPath = str(tmp_path / "roundtrip.xml")
    XkorXmlWriter(xmlPath, rp, [(uuid.uuid4(), ev)])
    assert os.path.getsize(xmlPath) > 0

    r = XkorXmlReader(xmlPath)
    events2 = r.events()
    rp2 = r.rpList()
    ev2 = events2[0][1]

    assert ev2.name() == ev.name()
    assert ev2.sport() == ev.sport()
    assert ev2.competition() == "standard"
    assert len(ev2.signupList().athletes()) == len(ev.signupList().athletes())
    assert ev2.results()[0] == ev.results()[0]
    assert abs(rp2.bonus("AAA") - rp.bonus("AAA")) < 1e-12
    a1 = sorted(a.name for a in ev.signupList().athletes())
    a2 = sorted(a.name for a in ev2.signupList().athletes())
    assert a1 == a2
    g1 = ev.groups()[0]
    g2 = ev2.groups()[0]
    assert g1.name == g2.name and g1.athletes == g2.athletes
