# FAQ

**Do files from the original xkoranate-CE still work?**

Yes. Event documents, signup lists, table generator files, and exported
results all load and save in the same format as the original C++ program —
you can move between them freely.

**Will my directory preferences carry over from the original program?**

Yes — see [Settings & file locations](settings.md). Settings are stored
under the same identifier the original used, so an existing install's
preferences are picked up automatically.

**Where do I report a bug or ask for a feature?**

Open an issue in the
[GitHub repo](https://github.com/NS-Sports/xkoranate-ce-python/issues/new/choose) —
there are separate templates for bug reports and feature requests. Check the
[roadmap](https://github.com/NS-Sports/xkoranate-ce-python/blob/main/ROADMAP.md)
first in case it's already tracked.

**Is scorination math the same as the original?**

Yes — matching the original's scorination math, output formatting, and file
formats byte-for-byte is a hard requirement for this port. If you find a
result that doesn't match what the original program would have produced,
that's a bug — please [report it](https://github.com/NS-Sports/xkoranate-ce-python/issues/new?template=bug_report.yml).

**Can I edit sport definitions or add a new sport?**

Sport files are plain XML under `sports/` and are hand-editable today. An
in-app editor for them is planned but not yet built — see
[issue #27](https://github.com/NS-Sports/xkoranate-ce-python/issues/27).
