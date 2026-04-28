---
name: rep-update
description: Enforces the multi-write checklist for rep state changes AND processes daily voice-memo field notes for the public reflection journal. Use this skill whenever a rep's status, blocker, next_step, or any other state field changes — whether from a Telegram update, todo completion, or brain dump — and when Robert sends a daily voice memo intended as a field-note entry.
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
- **Robert sends a daily voice memo / transcript intended as a field-note reflection** (treat any free-form reflective transcript that mentions one or more reps as a field-note candidate, not a rep update — see the Field Notes section below)

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
    pita:        # integer 1-10, operational lift (1=low, 10=high)
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
- **pita** — integer 1-10. Operational lift index. 1 = passive, 10 = high-touch daily ops. Dashboard renders color-coded badges.
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

## Rep Markdown File Format (`reps/NNN-name.md`)

Every rep has a companion file in `~/100reps/reps/`. When updating a rep, also update this file to stay in sync.

### Structure

```markdown
# Rep NNN — Name

**Status:** Idea|Assessed|Building|Live|PMF|Dead
**Repo:** [owner/repo](https://github.com/owner/repo)
**Website:** [domain.com](https://domain.com)

Summary paragraph.

## Next Steps

- Bulleted next actions

## Milestones

- YYYY-MM-DD: Event
```

### Rules

- **Title:** `# Rep NNN — Name` with em dash
- **Status:** Title case, must match reps.yaml
- **Repo/Website/App Store lines:** Include only when field exists in reps.yaml. Omit for null values.
- **Next Steps:** Include when reps.yaml `next_step` is not null
- **Milestones:** Include when reps.yaml `timeline` exists. Oldest first.
- **Dead reps:** Add `**Killed YYYY-MM-DD:** Reason.` after summary
- **No planning docs:** Detailed checklists, specs, etc. belong in the rep's dedicated repo, not here
- **If the file doesn't exist:** Create it following this format

---

## The Three-Write Checklist

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

### Write 2: Rep Markdown File

**Path:** `~/100reps/reps/NNN-name.md`

Update the rep file to reflect changes:
- Update **Status** line if status changed
- Update **Next Steps** section if next_step changed
- Add milestone entries if timeline changed
- For dead reps, add the kill line and remove Next Steps

### Write 3: Vault Main Note

**Path:** `~/second-brain/RW Vault/6 - Main Notes/<Rep Name>.md`

Append a dated entry to the note body, before the `# References` section:

```markdown
---

**YYYY-MM-DD:** <one-liner describing what changed and why>
```

If the update is substantive (new feature decision, pivot, major milestone), write a full paragraph in Robert's voice rather than a one-liner.

**Tag check:** Verify the Main Note's frontmatter `Tags:` line includes the rep's tag from `3 - Tags/` (e.g., `[[estate-sale-helper]]`). Add if missing.

**Cross-link check:** If the update references another rep or concept, add a `[[wikilink]]` in the body.

### Write 4: Validate + Git Commits

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

## Field Notes & Lessons Protocol

For daily reflection voice memos, follow this pipeline. The agent writes ONLY to `field-notes/`. Lessons are Robert's domain — never write to `lessons/`.

### Steps

1. **Receive** voice memo + transcript via Telegram.

2. **Sanitize** the transcript per public-field privacy rules. Same rules that apply to `next_step` and `blocker`:
   - No personal names (first + last). The existing `sanitizeNextStep` JS function in `docs/index.html` is the canonical reference for which name patterns must be stripped.
   - No email addresses, phone numbers, or private internal references.
   - When in doubt, strip. The journal is public.

3. **Identify rep references and tags.** Reps may be referenced by id ("rep 011"), name ("Estate Sale Helper"), or shorthand. Tags are themes — lowercase, hyphen-separated.

4. **Write `field-notes/YYYY-MM-DD.md`**:
   - If the file does NOT exist, create it with frontmatter:
     ```yaml
     ---
     date: YYYY-MM-DD
     reps: [<ids>]
     tags: [<tags>]
     mood: <optional one-word>
     ---
     ```
     Body: cleaned-up markdown of the transcript, with `[[rep:NNN]]` and `[[lesson:slug]]` wikilinks where appropriate.
   - If the file EXISTS for today, **append** to the body. Never overwrite. Append separator and timestamp heading:
     ```markdown

     ---

     ## YYYY-MM-DD HH:MM

     <new content>
     ```
     Frontmatter is preserved; merge new rep ids and tags into the arrays.

5. **Compare against existing lessons.** The agent NEVER writes to `lessons/`. Surface in the Telegram reply:
   - **Lessons reinforced:** if the entry restates an existing lesson, propose a `last_updated` bump, additions to `reps`, and any one-line evidence note. Robert decides whether to apply.
   - **New lesson candidates:** if the entry suggests a *new* lesson, propose a slug, title, one-paragraph rationale, and contributing rep ids. Robert decides whether to hand-create `lessons/<slug>.md`.

6. **Validate** before committing:
   ```bash
   python3 scripts/build_journal.py
   ```
   Must exit 0 and regenerate `docs/field-notes.json` and `docs/lessons.json`. If it fails, fix before committing.

7. **Commit and push** the field-note change:
   ```bash
   git -C ~/100reps add field-notes/YYYY-MM-DD.md docs/field-notes.json docs/lessons.json
   git -C ~/100reps commit -m "field-notes: YYYY-MM-DD reflection (reps NNN, NNN)"
   git -C ~/100reps push
   ```

8. **Reply to Robert** in Telegram with:
   - Entry written or appended
   - Reps tagged
   - Lessons reinforced (with proposed updates)
   - New lesson candidates
   - Anything sanitization stripped

### Key invariants

- The agent only writes to `field-notes/` (and the regenerated JSONs in `docs/`). Never to `lessons/`.
- Entries are append-only within a day.
- The build script must pass before commit. Treat its exit code as the gate.
- Public sanitization is non-negotiable.

---

## Quick Checklist

- [ ] reps.yaml read before writing
- [ ] reps.yaml updated with correct fields (including pita)
- [ ] reps.yaml validated with `npx js-yaml reps.yaml > /dev/null`
- [ ] Rep markdown file updated (or created if missing)
- [ ] Vault Main Note appended with dated entry
- [ ] Tags verified on Main Note
- [ ] All repos committed + pushed (100reps + second-brain)
- [ ] Confirmation sent to Robert
