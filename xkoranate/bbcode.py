import re

# Display-only post-processing of already-generated results text (see
# ROADMAP.md #36). We deliberately don't touch paradigm output-format
# strings (PORTING.md "What NOT to change") — instead these regexes
# recognise the handful of line shapes XkorAbstractH2HParadigm.outputLine()
# produces and wrap just the winning name in [b]...[/b]. Names are
# restricted to non-digit text so lines we can't confidently parse
# (Gaelic/Australian scores, period tables, draws) are left alone.
_DEF_BY_RE = re.compile(r"^(?P<loser>[^\d\n]+?) def\. by (?P<winner>[^\d\n]+?) \((?P<status>.+)\)$")
_DEF_RE = re.compile(r"^(?P<winner>[^\d\n]+?) def\. (?P<loser>[^\d\n]+?) \((?P<status>.+)\)$")
_SCORE_LINE_RE = re.compile(
    r"^(?P<home>.+?) (?P<homeScore>-?\d+(?:\.\d+)?)–(?P<awayScore>-?\d+(?:\.\d+)?) (?P<away>.+)$")


def boldWinnerLine(line):
    m = _DEF_BY_RE.match(line)
    if m:
        return line[:m.start("winner")] + "[b]%s[/b]" % m.group("winner") + line[m.end("winner"):]

    m = _DEF_RE.match(line)
    if m:
        return "[b]%s[/b]" % m.group("winner") + line[m.end("winner"):]

    m = _SCORE_LINE_RE.match(line)
    if m:
        homeScore = float(m.group("homeScore"))
        awayScore = float(m.group("awayScore"))
        if homeScore > awayScore:
            return "[b]%s[/b]" % m.group("home") + line[m.end("home"):]
        elif awayScore > homeScore:
            name, sep, tail = m.group("away").partition(" (")
            return line[:m.start("away")] + "[b]%s[/b]" % name + sep + tail

    return line


def boldWinners(text):
    return "\n".join(boldWinnerLine(line) for line in text.split("\n"))
