---
name: rep-update
description: Enforces the two-write checklist for rep state changes. Use this skill whenever a rep's status, blocker, next_step, or any other state field changes — whether from a Telegram update, todo completion, or brain dump containing rep progress. Never update reps.yaml without also updating the vault Main Note.
---

# Rep Update

Processes rep state changes with a mandatory two-write protocol. This ensures `reps.yaml` and the vault Main Note never drift.

**reps.yaml drives the live public dashboard at 100repsproject.com. A malformed file takes the dashboard offline. Follow every rule in this skill exactly.**

---

## When to Use

- Robert reports progress on a rep via Telegram
- A todo prefixed with "Rep NNN" is completed
- Any rep field changes (status, blocker, next_step, last_action, due)
- A brain dump contains rep-level progress or decisions

---

## Before Writing Anything

1. Read `~/100reps/reps.yaml` — confirm current state of the rep
2. If the Main Note does not exist, create it using brain-dump-processor conventions (frontmatter, status `#baby`, appropriate tags)
3. **Do not read the Main Note before appending** — it's an append-only log. Just append.

---

## reps.yaml Format Rules (MANDATORY)

These rules are non-negotiable. Every write to reps.yaml MUST conform to them.

### Field Schema — exact order, all required

```yaml
  - id:          # integer, sequential, never reuse, never change
    name:        # string, short project name
    status:      # string, one of: idea | assessed | building | live | pmf | dead
    summary:     # string, 1-2 sentences, plain text, no markdown, <200 chars
    next_step:   # string or null
    due:         # date (YYYY-MM-DD) or null
    blocker:     # string or null
    last_action: # date (YYYY-MM-DD), required
    repo:        # string "owner/repo" or null
```

Optional fields (appear after `repo` ONLY when present):

```yaml
    links:       # map — only public-facing URLs, never GitHub URLs
      website:   # URL or null
      app_store: # URL or null
      sales:     # URL or null
    timeline:    # array — chronological milestones
      - date:    # YYYY-MM-DD
        event:   # string, always quoted
```

### Field Rules

- **id** — sequential integer starting at 1. New reps get `max(id) + 1`. Never skip, reuse, or reassign.
- **status** — MUST be exactly one of (lowercase): `idea`, `assessed`, `building`, `live`, `pmf`, `dead`. Any other value breaks the dashboard.
- **summary** — plain text, 1-2 sentences, no markdown, no line breaks, under 200 characters.
- **next_step** — plain text or `null`. **PUBLIC FIELD.** Never include personal names (first + last), email addresses, phone numbers, or private internal references.
- **due** — ISO date `YYYY-MM-DD` or `null`. No datetime or timezone formats.
- **blocker** — plain text or `null`. **PUBLIC FIELD.** Same privacy rules as `next_step`.
- **last_action** — ISO date `YYYY-MM-DD`. Required. Update on EVERY change to the rep.
- **repo** — format `owner/repo` (not a full URL) or `null`.
- **links** — only `website`, `app_store`, `sales` keys. Omit the entire block if none. Never `links: {}`.
- **timeline** — each entry needs `date` + `event` (quoted). Oldest first. Omit the entire block if none. Never `timeline: []`.

### Formatting Rules

- **Indentation** — 2 spaces. No tabs. Fields indented 4 spaces from left margin.
- **Quoting** — no quotes on strings unless they contain special YAML characters (`: { } [ ] , & * # ? | - < > = ! % @`). Timeline `event` values always quoted.
- **Null values** — literal `null`. Never empty string, `~`, or omission.
- **Dates** — bare `YYYY-MM-DD` without quotes. Never datetime formats.
- **Field order** — maintain the exact order shown in the schema above.
- **Blank lines** — one blank line between rep entries. No blank lines within a rep entry.
- **No trailing whitespace.** One final newline at EOF.

### Operational Rules

- **Adding a rep** — append to end. Assign `id = max(existing ids) + 1`. Increment `meta.total`.
- **Removing a rep** — set `status: dead`. Do NOT delete entries.
- **Updating a rep** — change only the fields that need updating. Always update `last_action`.
- **Never add new top-level keys** — only `meta` and `reps` are valid.
- **Never add new fields to a rep** — if a new field is needed, coordinate with the dashboard code first.

---

## The Two-Write Checklist

### Write 1: reps.yaml

**Path:** `~/100reps/reps.yaml`

Update the relevant fields for the affected rep:

| Field | When to update |
|-------|---------------|
| `status` | idea / assessed / building / live / pmf / dead |
| `next_step` | When the next action changes |
| `blocker` | Set when blocked; set to `null` when cleared |
| `last_action` | Set to today's date (YYYY-MM-DD) on every update |
| `due` | When a deadline is set or changed |
| `summary` | When the project description materially changes |

**Do not touch** fields that haven't changed. Preserve all other rep entries exactly as-is.

### Write 2: Vault Main Note

**Path:** `~/second-brain/RW Vault/6 - Main Notes/<Rep Name>.md`

Append a dated entry to the note body, before the `# References` section:

```markdown
---

**YYYY-MM-DD:** <one-liner describing what changed and why>
```

If the update is substantive (new feature decision, pivot, major milestone), write a full paragraph in Robert's voice rather than a one-liner.

**Tag check:** Verify the Main Note's frontmatter `Tags:` line includes the rep's tag from `3 - Tags/` (e.g., `[[estate-sale-helper]]`). Add if missing.

**Cross-link check:** If the update references another rep or concept, add a `[[wikilink]]` in the body.

### Write 3: Validate + Git Commits

**Validate reps.yaml before committing.** A syntax error takes the dashboard offline.

```bash
python3 -c "import yaml; data=yaml.safe_load(open('$HOME/100reps/reps.yaml')); assert len(data['reps'])==data['meta']['total'], f'meta.total ({data[\"meta\"][\"total\"]}) != reps count ({len(data[\"reps\"])})'; print('VALID')"
```

If validation fails, fix the issue before proceeding. Do NOT commit invalid YAML.

Commit both the 100Reps repo (reps.yaml) and the vault:

```bash
git -C ~/100reps add -A && git -C ~/100reps commit -m "Rep NNN <Rep Name>: <summary of change>" && git -C ~/100reps push
```

```bash
git -C ~/second-brain add -A && git -C ~/second-brain commit -m "Rep NNN <Rep Name>: <summary of change>" && git -C ~/second-brain push
```

---

## Confirmation

After both writes and the commit, reply to Robert with:

1. **What changed in reps.yaml** — field: old value -> new value
2. **What was appended to the Main Note** — the dated entry or summary
3. **Tags/links added** — any new tags or cross-links
4. **Implications noticed** — if this update affects other reps (e.g., clearing a blocker that gates another rep), flag it

---

## Quick Checklist

- [ ] reps.yaml read before writing
- [ ] Main Note read (or created if missing)
- [ ] reps.yaml updated with correct fields
- [ ] Main Note appended with dated entry
- [ ] Tags verified on Main Note
- [ ] Both repos committed + pushed (100reps + second-brain)
- [ ] Confirmation sent to Robert
