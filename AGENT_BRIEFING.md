# Agent Briefing — Field Notes & Lessons (2026-04-28)

This document briefs Robert's local Telegram agent on the new Field Notes & Lessons pipeline. It supplements (not replaces) `skills/universal/rep-update/SKILL.md`. If the two ever conflict, **trust SKILL.md** — that's canonical. This file is an onboarding pointer.

## What changed

The 100Reps repo now has a public reflection journal. The `rep-update` skill at `skills/universal/rep-update/SKILL.md` has been extended with a Field Notes & Lessons protocol. **Re-sync the skill file** (`git pull` from your local clone of `100Reps-dashboard`, or refetch it from wherever you load skills) before running again.

## New responsibilities

When Robert sends you a daily voice memo / transcript, treat it as a **field-note** (not a rep update) if it's reflective rather than a state change. Heuristic: if it talks about *learnings*, *patterns*, *frustrations*, *what went wrong*, or *what's working*, it's a field note. If it says "rep 011 is now live" or "blocker cleared on rep 003", it's a rep update — handle as before.

## Field-note pipeline (8 steps)

1. **Receive** the voice memo + transcript via Telegram.

2. **Sanitize** the transcript per the same privacy rules that apply to `next_step` and `blocker`:
   - No personal names (first + last)
   - No email addresses
   - No phone numbers
   - No private internal references

   When in doubt, strip. The journal is publicly readable on 100repsproject.com.

3. **Identify** rep references and tags. Reps may be referenced by id ("rep 011"), name ("Estate Sale Helper"), or shorthand. Tags are themes — lowercase, hyphen-separated (e.g., `distribution`, `cold-outreach`, `pricing`, `hardware-qa`).

4. **Write** `field-notes/YYYY-MM-DD.md` in the `100Reps-dashboard` repo:
   - **If the file does NOT exist**, create it with this frontmatter:
     ```yaml
     ---
     date: YYYY-MM-DD
     reps: [<ids>]
     tags: [<tags>]
     mood: <optional one-word>
     ---
     ```
     Body: cleaned-up markdown of the transcript. Use `[[rep:NNN]]` and `[[lesson:slug]]` wikilinks where references make sense — they get rendered as live links by the build step.
   - **If the file EXISTS for today, APPEND**. Never overwrite. Preserve the existing frontmatter (merge new rep ids and tags into the arrays). Append separator + level-2 timestamp heading + new content:
     ```markdown

     ---

     ## YYYY-MM-DD HH:MM

     <new content>
     ```

5. **Compare against existing lessons** at `lessons/*.md`. **You NEVER write to `lessons/`.** Lessons are Robert's domain. Instead, surface in your Telegram reply:
   - **Lessons reinforced:** if the entry restates an existing lesson, propose a `last_updated` bump, additions to `reps`, and any one-line evidence note worth appending. Robert decides whether to apply.
   - **New lesson candidates:** if the entry suggests a *new* lesson, propose a slug, title, one-paragraph rationale, and contributing rep ids. Robert decides whether to hand-create the lesson file.

6. **Validate** before committing:
   ```bash
   cd ~/100reps && python3 scripts/build_journal.py
   ```
   Must exit 0 and regenerate `docs/field-notes.json` and `docs/lessons.json`. If it fails, fix the issue (almost always a malformed frontmatter) before committing. A broken file takes the journal panel offline.

   First-time setup if `python3 scripts/build_journal.py` fails with `ModuleNotFoundError`:
   ```bash
   cd ~/100reps && pip3 install -r requirements.txt
   # or, if PEP 668 blocks system pip:
   python3 -m venv venv && ./venv/bin/pip install -r requirements.txt
   # then use ./venv/bin/python3 scripts/build_journal.py
   ```

7. **Commit and push** the field-note plus regenerated JSONs:
   ```bash
   cd ~/100reps
   git add field-notes/YYYY-MM-DD.md docs/field-notes.json docs/lessons.json
   git commit -m "field-notes: YYYY-MM-DD reflection (reps NNN, NNN)"
   git push
   ```
   The GH Action `build-journal.yml` will also run the build on push and commit any drift back. Your local build avoids the round-trip and confirms validity before pushing.

8. **Reply to Robert** in Telegram with a structured summary:
   - Entry written or appended (which file, mood if set)
   - Reps tagged
   - Lessons reinforced (with proposed updates)
   - New lesson candidates (with proposed slug/title/rationale)
   - Anything sanitization stripped (so Robert can confirm nothing important got dropped)

## Key invariants (do not violate)

| Rule | Why |
|------|-----|
| Only write to `field-notes/`. Never to `lessons/`. | Lessons are public canon — Robert curates them by hand. |
| Entries are append-only within a day. | Preserves morning-vs-evening reflection arcs in one entry. |
| `python3 scripts/build_journal.py` must exit 0 before commit. | Treat exit code as the gate. Live site goes offline on broken JSON. |
| Privacy sanitization is non-negotiable. | The journal is on a public domain; the rules match `next_step`/`blocker`. |
| Frontmatter date must equal the filename (`YYYY-MM-DD.md`). | Build step rejects mismatches. |

## Quick reference

**File schemas** (also in `FIELD_NOTES_SPEC.md`):

Field note:
```yaml
---
date: 2026-04-28
reps: [11, 14]
tags: [distribution, cold-outreach]
mood: stuck     # optional
---
Body markdown. [[rep:011]] and [[lesson:distribution-beats-craft]] are live wikilinks.
```

Lesson (FYI — you propose, Robert writes):
```yaml
---
slug: distribution-beats-craft
title: Distribution Beats Craft for Physical-Product Reps
reps: [9, 11, 14]
tags: [distribution]
first_seen: 2026-03-12
last_updated: 2026-04-28
---
```

**Where things live:**
- `field-notes/YYYY-MM-DD.md` — your writes
- `lessons/<slug>.md` — Robert's writes only
- `scripts/build_journal.py` — validator + JSON generator
- `docs/field-notes.json`, `docs/lessons.json` — generated; check in, don't hand-edit
- `FIELD_NOTES_SPEC.md` — full schema reference
- `skills/universal/rep-update/SKILL.md` — your updated operating manual

## Confirmation

After your first field-note write, please reply with:
1. Which file you created/appended
2. Which reps it tagged
3. Confirmation that `python3 scripts/build_journal.py` exited 0 locally
4. Any lesson reinforcements or new-lesson candidates you noticed
