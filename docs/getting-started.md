# Getting started

## Download

Grab the build for your platform from the
[Releases page](https://github.com/NS-Sports/xkoranate-ce-python/releases).
Each release ships a build for macOS, Windows, and Linux.

| Platform | Archive | Run |
|---|---|---|
| macOS | `xkoranate-<version>-macos.zip` | Unzip, then open `xkoranate.app` |
| Windows | `xkoranate-<version>-windows.zip` | Unzip, then run `xkoranate\xkoranate.exe` |
| Linux | `xkoranate-<version>-linux.tar.gz` | Extract, then run `xkoranate/xkoranate` |

!!! note "Unsigned builds"
    These builds aren't code-signed or notarized, so your OS will likely warn
    you the first time you open one (macOS Gatekeeper, Windows SmartScreen).
    You'll need to explicitly allow the app to run — right-click → Open on
    macOS, or "More info" → "Run anyway" on Windows.

## The main window

When you launch xkoranate you land on the main window: a sidebar on the left
listing your **Events** and your **Bonuses** configuration, and a large
central area that shows whichever one is selected. A toolbar across the top
gives you the core actions:

| Button | Does |
|---|---|
| New file | Start a fresh document |
| Open file | Load a saved `.xml` document |
| Save / Save as | Save the current document |
| Table generator | Open the standalone [table generator](table-generator.md) window |
| Dark mode | Toggle light/dark theme (also in the **View** menu) |

A single xkoranate document (the `.xml` file you save) can contain **multiple
events** plus **one bonuses configuration** shared across all of them — you
don't need a separate file per event.

## What's next

- [Building an event](building-an-event.md) walks through the 5-step wizard
  used to set up and run a scorination.
- [Table generator](table-generator.md) covers the standalone tool for
  turning match results into league standings.
- [RP bonuses](rp-bonuses.md) explains the per-nation bonus configuration.
