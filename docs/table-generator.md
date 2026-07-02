# Table generator

The table generator is a standalone window for turning a set of match results
into league standings. It's independent of the event editor — open it with
the **Table generator** button in the main toolbar (or the **View** menu),
and it's useful even for results that weren't produced by xkoranate at all,
as long as they're in the expected format.

## Workflow

1. **Import match results…** — load a `.txt` results file (this can be a
   file exported from the event editor's Scorinate step, or hand-authored).
2. Configure scoring:
      - **Win / Draw / Loss** point values
      - **Draws** checkbox — include a draws column, or disallow draws
        entirely
      - **Results grid** checkbox — show a full grid of head-to-head results
        alongside the standings
      - The unit label for the "for/against" columns (**Goals**, **Korfs**,
        **Points**, or **Runs**) — pick whichever matches your sport
      - Column width, for formatting the plaintext output
3. **Generate table** — renders the standings from the imported results using
   your settings.
4. **Save file** / **Save file as…** — save the table configuration as a
   `.xml` file so you can reload and regenerate it later (e.g. after
   importing a new matchday's results).

The rendered table is plain, monospace-formatted text — ready to paste
straight into a forum post.
