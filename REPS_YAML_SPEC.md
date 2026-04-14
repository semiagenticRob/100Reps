# reps.yaml Specification

This file is the canonical source of truth for the 100 Reps Project. It drives the public dashboard at 100repsproject.com. **Breaking changes to this file will break the live website.** Follow these rules exactly.

---

## File Structure

The file has two top-level keys: `meta` and `reps`.

```yaml
meta:
  total: 14       # integer — current count of reps, must match length of reps array
  target: 100     # integer — goal count, do not change

reps:
  - id: 1
    ...
```

**Always update `meta.total`** when adding or removing a rep.

---

## Rep Schema

Every rep entry MUST have these fields in this exact order:

```yaml
  - id:          # integer, sequential, never reuse, never change
    name:        # string, short project name
    status:      # string, one of: idea | assessed | building | live | pmf | dead
    pita:        # integer 1-10, Pain In The Ass index (operational lift)
    summary:     # string, 1-2 sentences describing the project
    next_step:   # string or null
    due:         # date (YYYY-MM-DD) or null
    blocker:     # string or null
    last_action: # date (YYYY-MM-DD), required — when this rep was last touched
    repo:        # string "owner/repo" or null — GitHub repo reference
```

These fields are OPTIONAL and appear after `repo` when present:

```yaml
    links:       # map of asset URLs (only public-facing properties)
      website:   # URL or null
      app_store: # URL or null
      sales:     # URL or null
    timeline:    # array of milestone entries
      - date:    # date (YYYY-MM-DD)
        event:   # string, quoted, describing the milestone
```

---

## Rules

### Field Rules

1. **id** — Sequential integer starting at 1. Never skip, reuse, or reassign an ID. New reps get `max(id) + 1`.

2. **status** — MUST be exactly one of these six values (lowercase):
   - `idea` — concept only, no work started
   - `assessed` — researched/validated, decision pending
   - `building` — active development
   - `live` — shipped and available to users
   - `pmf` — product-market fit achieved
   - `dead` — abandoned, will not proceed
   
   Any other value will break the dashboard filters and color coding.

3. **pita** — Integer 1-10. "Pain In The Ass" index — operational lift to continuously run this rep. 1 = low-touch passive, 10 = high-touch daily ops. The dashboard uses this for color-coded badges (green→red scale) and sorting.

4. **summary** — Plain text, 1-2 sentences. No markdown, no line breaks. Keep under 200 characters.

5. **next_step** — Plain text or `null`. **This field is displayed publicly on the dashboard.** A privacy sanitizer strips obvious names and contact info, but do not rely on it. Never put:
   - Personal names (first + last)
   - Email addresses or phone numbers
   - Private internal references people outside the project shouldn't see
   
   Good: `"Launch promotion campaign — social media, ASO, partnerships"`
   Bad: `"Email John Smith at john@example.com about the deal"`

6. **due** — ISO date `YYYY-MM-DD` or `null`. Do not use datetime or timezone formats.

7. **blocker** — Plain text or `null`. Displayed in the public blocker ticker at the bottom of the dashboard. Same privacy rules as `next_step`.

8. **last_action** — ISO date `YYYY-MM-DD`. Required. Update this every time ANY change is made to the rep. The dashboard uses this for staleness detection.

9. **repo** — Format `owner/repo` (e.g., `semiagenticRob/estate-sale-helper`). Not a full URL. Or `null` if no repo exists. The dashboard uses this to fetch git commit history from the GitHub API.

10. **links** — Only public-facing properties (websites, app stores, sales pages). **Never include GitHub URLs** — the `repo` field handles that separately. Allowed keys:
    - `website` — the project's public website
    - `app_store` — iOS/Android app store listing
    - `sales` — sales or landing page if different from website
    
    Omit the entire `links` block if there are no public links. Do not include empty maps (`links: {}`).

11. **timeline** — Manual milestone entries for key project events. Each entry needs `date` (YYYY-MM-DD) and `event` (quoted string). Keep entries chronological (oldest first). The dashboard merges these with git commit history fetched from the `repo`.
    
    Omit the entire `timeline` block if there are no milestones. Do not include empty arrays (`timeline: []`).

### Formatting Rules

12. **Indentation** — 2 spaces. No tabs. Every field indented 4 spaces from the left margin (nested under the `- id:` list item).

13. **Quoting** — String values do NOT need quotes unless they contain special YAML characters (`: { } [ ] , & * # ? | - < > = ! % @`). Timeline `event` values should always be quoted.

14. **Null values** — Use the literal `null`, not empty string, not `~`, not omission.

15. **Dates** — Always `YYYY-MM-DD`. Bare dates without quotes. YAML parsers (including js-yaml) auto-parse these as Date objects. Never use datetime formats like `2026-04-08T00:00:00Z`.

16. **Field order** — Maintain the exact field order shown in the schema above. The dashboard doesn't depend on order, but consistency prevents merge conflicts and keeps diffs clean.

17. **Blank lines** — One blank line between rep entries. No blank lines within a rep entry.

18. **No trailing whitespace** or trailing newlines beyond one final newline at EOF.

### Operational Rules

19. **Adding a rep** — Append to the end of the `reps` array. Assign `id = max(existing ids) + 1`. Increment `meta.total`. Include all required fields.

20. **Removing a rep** — Set `status: dead` instead of deleting. Decrement `meta.total` only if you truly delete the entry (not recommended). Dead reps are dimmed on the dashboard and preserved for history.

21. **Updating a rep** — Change only the fields that need updating. Always update `last_action` to today's date when making any change.

22. **Do not rename or add top-level keys** — The only valid top-level keys are `meta` and `reps`. Adding others will not break the parser but creates drift.

23. **Do not add new fields to a rep** — The dashboard ignores unknown fields, but they add noise and may cause confusion. If a new field is needed, coordinate with the dashboard code in `docs/index.html` first.

24. **Validate before committing** — Run `npx js-yaml reps.yaml > /dev/null` or equivalent to confirm the file is valid YAML. A syntax error here takes the entire dashboard offline.

---

## Example: Adding a New Rep

```yaml
  - id: 15
    name: My New Project
    status: idea
    pita: 3
    summary: One-line description of the project.
    next_step: null
    due: null
    blocker: null
    last_action: 2026-04-10
    repo: null
```

Then update `meta.total: 15`.

## Example: Promoting a Rep to Live with Links

```yaml
  - id: 15
    name: My New Project
    status: live
    pita: 5
    summary: One-line description of the project.
    next_step: Launch marketing push
    due: null
    blocker: null
    last_action: 2026-04-10
    repo: semiagenticRob/my-new-project
    links:
      website: https://mynewproject.com
      app_store: https://apps.apple.com/us/app/my-new-project/id1234567890
    timeline:
      - date: 2026-03-15
        event: "Idea conceived"
      - date: 2026-04-01
        event: "MVP complete"
      - date: 2026-04-10
        event: "Launched publicly"
```

---

## Rep Markdown Files (`reps/NNN-name.md`)

Each rep has a companion markdown file in the `reps/` directory. These are human-readable summaries — not dashboards, not planning docs. Keep them concise.

### Filename Convention

`NNN-name.md` where NNN is the zero-padded rep id (e.g., `001-pipe-acquisition.md`, `016-stock-up-dinners.md`). Name is lowercase, hyphenated.

### Required Structure

```markdown
# Rep NNN — Name

**Status:** Idea|Assessed|Building|Live|PMF|Dead
**Repo:** [owner/repo](https://github.com/owner/repo)
**Website:** [domain.com](https://domain.com)
**App Store:** [App Name](https://apps.apple.com/...)

Summary paragraph. 1-3 sentences.

## Section(s)

Optional content sections (Progress, Notes, Assessment, etc.). Keep relevant to the rep's current state.

## Next Steps

- Bulleted list of next actions (match reps.yaml next_step + any detail)

## Milestones

- YYYY-MM-DD: Event description (match reps.yaml timeline entries)
```

### Rules

1. **Title** — Always `# Rep NNN — Name` with em dash.
2. **Status** — Title case, must match reps.yaml `status` field. No extra metadata on the status line (no `| **Type:** ...`).
3. **Repo/Website/App Store lines** — Include only when the corresponding field exists in reps.yaml. Repo format: `[owner/repo](full URL)`. Omit lines for null values.
4. **Summary** — Must align with reps.yaml `summary`. Can be slightly expanded but should not contradict.
5. **Next Steps** — Include when reps.yaml `next_step` is not null. Can expand with additional detail beyond the yaml one-liner.
6. **Milestones** — Include when reps.yaml `timeline` exists. Format: `- YYYY-MM-DD: Event`. Oldest first.
7. **Dead reps** — Add a bolded kill line after the summary: `**Killed YYYY-MM-DD:** Reason.` Preserve architecture/history sections for reference.
8. **No planning docs** — Detailed planning, checklists, ingredient lists, etc. belong in the rep's dedicated repo, not in the rep markdown file. The rep file is a summary card.
9. **Keep in sync** — When reps.yaml changes, the rep file should be updated to match (status, next steps, milestones). The rep-update skill enforces this.
