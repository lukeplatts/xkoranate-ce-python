# Settings & file locations

xkoranate doesn't have a separate settings/preferences dialog. Instead, it
remembers the last folder you used for each kind of file, and defaults each
one to your home directory the first time you run it:

| What | Remembered when you… |
|---|---|
| Event directory | Open/save an event document (`.xml`) |
| Signup list directory | Import a signup list (`.txt`) in the Signups step |
| Result export directory | Export results (`.txt`) from the Scorinate step |
| Result import directory | Import match results (`.txt`) into the table generator |
| Table directory | Open/save a table generator configuration (`.xml`) |

These are stored using Qt's `QSettings`, under the same
`thirdgeek.com`/`xkoranate` identifier the original C++ xkoranate-CE used —
so if you're upgrading from the original program, your directory preferences
carry over automatically. Concretely, that means:

- **macOS**: `~/Library/Preferences/com.thirdgeek.xkoranate.plist`
- **Windows**: `HKEY_CURRENT_USER\Software\thirdgeek.com\xkoranate` (registry)
- **Linux**: `~/.config/thirdgeek.com/xkoranate.conf`

## Sport definitions

The `sports/` folder that ships alongside xkoranate contains the sport
definition files — plain XML, one per sport, describing its paradigm and
default options. They're user-editable if you know what you're doing, though
there's no in-app editor for them yet (tracked in
[issue #27](https://github.com/NS-Sports/xkoranate-ce-python/issues/27)).
