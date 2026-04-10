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

3. **summary** — Plain text, 1-2 sentences. No markdown, no line breaks. Keep under 200 characters.

4. **next_step** — Plain text or `null`. **This field is displayed publicly on the dashboard.** A privacy sanitizer strips obvious names and contact info, but do not rely on it. Never put:
   - Personal names (first + last)
   - Email addresses or phone numbers
   - Private internal references people outside the project shouldn't see
   
   Good: `"Launch promotion campaign — social media, ASO, partnerships"`
   Bad: `"Email John Smith at john@example.com about the deal"`

5. **due** — ISO date `YYYY-MM-DD` or `null`. Do not use datetime or timezone formats.

6. **blocker** — Plain text or `null`. Displayed in the public blocker ticker at the bottom of the dashboard. Same privacy rules as `next_step`.

7. **last_action** — ISO date `YYYY-MM-DD`. Required. Update this every time ANY change is made to the rep. The dashboard uses this for staleness detection.

8. **repo** — Format `owner/repo` (e.g., `semiagenticRob/estate-sale-helper`). Not a full URL. Or `null` if no repo exists. The dashboard uses this to fetch git commit history from the GitHub API.

9. **links** — Only public-facing properties (websites, app stores, sales pages). **Never include GitHub URLs** — the `repo` field handles that separately. Allowed keys:
   - `website` — the project's public website
   - `app_store` — iOS/Android app store listing
   - `sales` — sales or landing page if different from website
   
   Omit the entire `links` block if there are no public links. Do not include empty maps (`links: {}`).

10. **timeline** — Manual milestone entries for key project events. Each entry needs `date` (YYYY-MM-DD) and `event` (quoted string). Keep entries chronological (oldest first). The dashboard merges these with git commit history fetched from the `repo`.
    
    Omit the entire `timeline` block if there are no milestones. Do not include empty arrays (`timeline: []`).

### Formatting Rules

11. **Indentation** — 2 spaces. No tabs. Every field indented 4 spaces from the left margin (nested under the `- id:` list item).

12. **Quoting** — String values do NOT need quotes unless they contain special YAML characters (`: { } [ ] , & * # ? | - < > = ! % @`). Timeline `event` values should always be quoted.

13. **Null values** — Use the literal `null`, not empty string, not `~`, not omission.

14. **Dates** — Always `YYYY-MM-DD`. Bare dates without quotes. YAML parsers (including js-yaml) auto-parse these as Date objects. Never use datetime formats like `2026-04-08T00:00:00Z`.

15. **Field order** — Maintain the exact field order shown in the schema above. The dashboard doesn't depend on order, but consistency prevents merge conflicts and keeps diffs clean.

16. **Blank lines** — One blank line between rep entries. No blank lines within a rep entry.

17. **No trailing whitespace** or trailing newlines beyond one final newline at EOF.

### Operational Rules

18. **Adding a rep** — Append to the end of the `reps` array. Assign `id = max(existing ids) + 1`. Increment `meta.total`. Include all required fields.

19. **Removing a rep** — Set `status: dead` instead of deleting. Decrement `meta.total` only if you truly delete the entry (not recommended). Dead reps are dimmed on the dashboard and preserved for history.

20. **Updating a rep** — Change only the fields that need updating. Always update `last_action` to today's date when making any change.

21. **Do not rename or add top-level keys** — The only valid top-level keys are `meta` and `reps`. Adding others will not break the parser but creates drift.

22. **Do not add new fields to a rep** — The dashboard ignores unknown fields, but they add noise and may cause confusion. If a new field is needed, coordinate with the dashboard code in `docs/index.html` first.

23. **Validate before committing** — Run `python3 -c "import yaml; yaml.safe_load(open('reps.yaml'))"` or equivalent to confirm the file is valid YAML. A syntax error here takes the entire dashboard offline.

---

## Example: Adding a New Rep

```yaml
  - id: 15
    name: My New Project
    status: idea
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
