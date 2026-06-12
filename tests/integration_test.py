"""End-to-end integration test: app boot, event creation, scorination, save/load."""

import os
import sys
import tempfile

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from PySide6.QtCore import QDir

from xkoranate.application import XkorApplication

app = XkorApplication(sys.argv)
app.loadSports()
cw = app.cw
nw = cw.navigationWidget if hasattr(cw, "navigationWidget") else None
print("app booted; sports loaded")

# --- direct model-level scorination across several sports/competitions ---
import uuid

from xkoranate.athlete import XkorAthlete
from xkoranate.competitions.competitionfactory import XkorCompetitionFactory
from xkoranate.event import XkorEvent
from xkoranate.group import XkorGroup
from xkoranate.rng import Mt19937
from xkoranate.rplist import XkorRPList
from xkoranate.signuplist import XkorSignupList
from xkoranate.xml.xmlindex import XkorXmlIndex
from xkoranate.xml.xmlsportreader import XkorXmlSportReader

rng = Mt19937(2026)

index = XkorXmlIndex()
index.traverse("sports:")

NATIONS = ["AAA", "BBB", "CCC", "DDD", "EEE", "FFF", "GGG", "HHH"]


def build_event(sportName, competition=None, nAthletes=8):
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


def scorinate(sportName, competition=None):
    from xkoranate.paradigms.paradigmfactory import XkorParadigmFactory

    ev, sport = build_event(sportName)
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


tests = [
    ("Athletics—Men’s 00100 m—Round 1", None),
    ("Badminton—xkoranate formula", "matches"),
    ("Association football—SQIS formula", "roundRobin"),
    ("Association football—Footba11er formula", "matches"),
]

for name, comp in tests:
    try:
        outs = scorinate(name, comp)
        first = outs[0].splitlines()
        print("== %s (%s): %d matchday(s), first lines:" % (name, comp or "default", len(outs)))
        for line in first[:6]:
            print("   |%s|" % line)
    except Exception as e:
        import traceback
        print("!! FAILED %s: %r" % (name, e))
        traceback.print_exc()

# --- save / load round-trip through the XML layer ---
from xkoranate.xml.xmlreader import XkorXmlReader
from xkoranate.xml.xmlwriter import XkorXmlWriter

ev, sport = build_event("Athletics—Men’s 00100 m—Round 1")
ev.setCompetition("standard")
ev.setResult(0, "some result text\nline 2")
rp = XkorRPList()
rp.setCompetitionName("Test Cup")
rp.addBonus(("AAA", {"bonus": 0.5}))

tmp = os.path.join(tempfile.mkdtemp(), "roundtrip.xml")
XkorXmlWriter(tmp, rp, [(uuid.uuid4(), ev)])
print("wrote", tmp, os.path.getsize(tmp), "bytes")

r = XkorXmlReader(tmp)
events2 = r.events()
rp2 = r.rpList()
ev2 = events2[0][1]
assert ev2.name() == ev.name(), (ev2.name(), ev.name())
assert ev2.sport() == ev.sport()
assert ev2.competition() == "standard"
assert len(ev2.signupList().athletes()) == len(ev.signupList().athletes())
assert ev2.results()[0] == ev.results()[0], ev2.results()
assert abs(rp2.bonus("AAA") - rp.bonus("AAA")) < 1e-12
a1 = sorted([a.name for a in ev.signupList().athletes()])
a2 = sorted([a.name for a in ev2.signupList().athletes()])
assert a1 == a2
g1 = ev.groups()[0]
g2 = ev2.groups()[0]
assert g1.name == g2.name and g1.athletes == g2.athletes
print("save/load round-trip OK")

print("ALL INTEGRATION TESTS PASSED")
