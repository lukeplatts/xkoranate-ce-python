# xkoranate-CE Python port — conventions

This project is a faithful Python/PySide6 port of the Qt4/C++ xkoranate-CE
(source kept at /tmp/xkoranate-src). The goal is **behavior preservation**,
not modernization. Port line-by-line where possible.

## Layout

C++ `src/foo/bar.{h,cpp}` → Python `xkoranate/foo/bar.py` (lowercase, same name).
One C++ class pair (.h/.cpp) = one Python module. Class names unchanged
(`XkorSport`, `XkorAbstractParadigm`, …).

## Naming

- Keep Qt-style **camelCase method names** exactly as in C++ (`setName`,
  `paradigmOptions`, `makeStartList`). Do not snake_case them.
- Private members `m_foo` / bare members keep their C++ names.
- Overloaded C++ methods: collapse into one Python method with default
  arguments where possible (e.g. `individualScore(index, skill=None)`),
  otherwise suffix (`randWeighted`, `randWeightedH2H`, `randWeightedFull` —
  see sport.py which is already ported).

## Type mapping

| C++ | Python |
|---|---|
| QString | str ("" for QString::null; use truthiness for isEmpty/null checks) |
| QHash<QString,QVariant>, QMap | dict |
| QList, QVector, QStringList | list |
| QPair | 2-tuple |
| QVariant | plain Python value (str/int/float/bool/list/uuid) |
| QUuid | uuid.UUID or None for null; `id.isNull()` → `id is None` |
| QMap<double,double> (sorted!) | dict; iterate `sorted(d.items())` (see sport.py transformNumber) |
| std::tr1::mt19937 | random.Random (see xkoranate/rng.py) |

## QVariant semantics — use xkoranate.variant helpers

Sport XML options arrive as **strings**; C++ code calls `.toDouble()`,
`.toInt()`, `.toBool()`, `.toList()` etc. on them. Port these calls with the
helpers in `xkoranate/variant.py`:

    opt.value("resultWidth", 10).toInt()  →  toInt(self.opt.get("resultWidth", 10))
    v.toString()   → toString(v)
    v.toDouble()   → toDouble(v)   # returns 0.0 on parse failure, like Qt
    v.toBool()     → toBool(v)     # "", "0", "false" → False; other strings True
    v.toList()     → toList(v)     # non-list values → [] (Qt semantics)
    v.toStringList() → toStringList(v)

`QVariant::type() == QVariant::List` → `isinstance(v, list)`.

## Implicit sharing / value semantics (THE #1 PORT BUG)

Qt containers and Xkor value classes copy on assignment; Python uses
references. Whenever C++…

- copies a struct (`XkorResult r = *i;`, `XkorAthlete a = ath;`) → use
  `r = i.clone()` (core classes provide `.clone()`).
- returns a member container from a getter that callers then modify → return
  `list(self.x)` / `dict(self.x)` shallow copy. When in doubt, copy.
- passes a container by value and mutates it inside → copy at function entry.

Shallow copies are usually right because contained values are str/float;
clone() the contained Xkor objects when the code mutates them.

## Qt classes

- UI: PySide6 (QtWidgets/QtCore/QtGui). Signals: `Signal(...)` class attrs;
  `emit foo(x)` → `self.foo.emit(x)`; `connect(a, SIGNAL(t()), b, SLOT(u()))`
  → `a.t.connect(b.u)`.
- `tr("x")` → plain string `"x"`.
- `qDebug() << ...` → `print(..., file=sys.stderr)`.
- XML: keep QXmlStreamReader/QXmlStreamWriter from PySide6.QtCore for a
  mechanical port. Note: `readElementText()`, `attributes().value()` return
  str directly in PySide6. QStringRef → str.
- `QIcon(":/icons/name")` → `from xkoranate.icons import icon; icon("name")`.
- QSettings("thirdgeek.com", "xkoranate") — keep identical so user settings
  carry over.
- Search-path URLs like `"sports:badminton"`, `"events:foo.xml"` — keep; we
  register the same Qt search paths via `QDir.setSearchPaths` (application.py).
- `QString::number(n, 'f', digits)` → `f"{n:.{digits}f}"`;
  `QString::number(int)` → `str()`; `.leftJustified(w)` → `.ljust(w)`;
  `.rightJustified(w)` → `.rjust(w)`.
- `QVariant(int)` stored then compared/used as number stays int; XML reads
  produce str — keep whatever the C++ stores.

## RNG

`xkoranate/rng.py` provides `Mt19937`, mimicking `std::tr1::mt19937`:
`r()` → `r.next32()` (32-bit uint), `r.min()`/`r.max()` constants. Sport's
`randUniform` = `next32() / 4294967295`. Seed from time like the C++ does.
A single shared instance is used by the app (created in centralwidget, passed
via `setPRNG`).

## Exceptions

C++ throw-specs disappear. `XkorFileNotFoundException`,
`XkorSearchFailedException` are in `xkoranate/exceptions.py`. C++
`catch(XkorSearchFailedException) {}` → `except XkorSearchFailedException: pass`.

## Virtual methods / abstract classes

Pure virtual (`= 0`) → raise NotImplementedError in the base. Keep the full
inheritance hierarchy. C++ functors (`operator()(a, b)`) → `__call__`.

## Iterator idioms

- `QHash::iterator i; i.key()/i.value()` → `for k, v in d.items()`. If the
  loop **mutates** the dict, iterate `list(d.items())`.
- `qSort(vec.begin(), vec.end(), comp)` where comp is a result comparator →
  `vec.sort(key=functools.cmp_to_key(...))` or
  `sorted(vec, key=cmp_to_key(lambda a, b: -1 if comp(a, b) else (1 if comp(b, a) else 0)))`.
  Note C++ qSort is NOT stable; qStableSort IS. Python sort is stable — fine
  for both.
- `std::random_shuffle(v.begin(), v.end())` → shared-RNG shuffle helper.

## What NOT to change

- All scorination math, constants, output-format strings (padding widths,
  separators, medal strings, etc.) must match the C++ byte-for-byte.
- Hash-iteration *order* differences are acceptable (C++ QHash order was
  arbitrary too), but where C++ iterates a QMap (sorted), Python must sort.
