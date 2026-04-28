# Agent Briefing — Field Notes & Lessons (rev 2026-04-28b)

This document briefs Robert's local Telegram agent on the Field Notes & Lessons pipeline. It supplements `skills/universal/rep-update/SKILL.md`. If the two ever conflict, **trust SKILL.md** — that's canonical.

## What changed

The 100Reps repo has a public reflection journal. The `rep-update` skill has been extended with a Field Notes & Lessons protocol. **Always start a session with `git pull`** — your clone is probably stale.

## Architectural ground truth

- **The agent commits markdown source only.** Never commit `docs/field-notes.json` or `docs/lessons.json` — those are generated artifacts.
- **The GitHub Action is the sole writer of the JSON files.** On every push to main that touches `field-notes/`, `lessons/`, `scripts/build_journal.py`, or `requirements.txt`, the action `.github/workflows/build-journal.yml` runs the build script and commits regenerated JSONs.
- **Local validation is a fast-feedback nice-to-have, not a hard requirement.** If your container has no python3, skip it — push the markdown, let the action validate. Worst case: the action fails on bad markdown, which means the journal panel keeps showing the previous-good state until you fix the markdown. The dashboard does not break.
- **The line of last defense is the action's exit code.** If the action ever fails on main, fix the offending markdown immediately or revert the bad commit.

## New responsibility

When Robert sends you a daily voice memo / transcript, treat it as a **field-note** (not a rep update) if it's reflective rather than a state change. Heuristic: if it talks about *learnings*, *patterns*, *frustrations*, *what went wrong*, or *what's working*, it's a field note. If it says "rep 011 is now live" or "blocker cleared on rep 003", it's a rep update — handle as before.

## Field-note pipeline

### 0. Sync first

```bash
cd ~/100reps && git pull --ff-only origin main
```

If `--ff-only` fails because you have local commits, rebase: `git pull --rebase origin main`. If conflicts arise, surface them to Robert — do not auto-resolve.

### 1. Receive

Voice memo + transcript via Telegram.

### 2. Sanitize

Strip per public-field privacy rules:
- No personal names (first + last)
- No email addresses
- No phone numbers
- No private internal references

When in doubt, strip. The journal is publicly readable on 100repsproject.com.

### 3. Identify rep references and tags

Reps may be referenced by id ("rep 011"), name ("Estate Sale Helper"), or shorthand. Tags are themes — lowercase, hyphen-separated (e.g., `distribution`, `cold-outreach`, `pricing`, `hardware-qa`).

### 4. Write `field-notes/YYYY-MM-DD.md`

**If the file does NOT exist**, create it with this frontmatter:

```yaml
---
date: YYYY-MM-DD
reps: [<ids>]
tags: [<tags>]
mood: <optional one-word>
---
```

Body: cleaned-up markdown of the transcript. Use `[[rep:NNN]]` and `[[lesson:slug]]` wikilinks where references make sense — they get rendered as live links by the build step.

**If the file EXISTS for today, APPEND.** Never overwrite. Preserve the existing frontmatter (you may add new rep ids and tags to the arrays — never remove). Append separator + level-2 timestamp heading + new content:

```markdown

---

## YYYY-MM-DD HH:MM

<new content>
```

### 5. Compare against existing lessons

Read `lessons/*.md`. **You NEVER write to `lessons/`.** Lessons are Robert's domain. Surface in your Telegram reply:

- **Lessons reinforced:** if the entry restates an existing lesson, propose a `last_updated` bump, additions to `reps`, and any one-line evidence note worth appending. Robert decides.
- **New lesson candidates:** propose a slug, title, one-paragraph rationale, and contributing rep ids. Robert decides whether to hand-create the lesson file.

### 6. Self-validate (best-effort, not a gate)

Run whichever of these is available in your environment, in order of preference:

**(a) Full validation if `python3` and the build script are present:**
```bash
cd ~/100reps && python3 scripts/build_journal.py
```
Exit 0 confirms the markdown parses and renders. Errors usually point at malformed frontmatter or filename/date mismatch. If you see `ModuleNotFoundError`, the deps aren't installed:
```bash
pip3 install -r requirements.txt
# or, if PEP 668 blocks system pip:
python3 -m venv venv && ./venv/bin/pip install -r requirements.txt
./venv/bin/python3 scripts/build_journal.py
```

**(b) YAML-only check if `python3` is available but `scripts/build_journal.py` is missing or deps fail:**
```bash
python3 -c "import yaml,sys; t=open('field-notes/YYYY-MM-DD.md').read(); fm=t.split('---',2)[1]; yaml.safe_load(fm); print('frontmatter VALID')"
```

**(c) Skip self-validation if no python3.** This is fine. Push, then check the GH Action result and react to any failure.

In all cases: do NOT block the field-note from being committed because of a missing-python environment. The action is the gate.

### 7. Commit and push — markdown ONLY

```bash
cd ~/100reps
git add field-notes/YYYY-MM-DD.md
git commit -m "field-notes: YYYY-MM-DD reflection (reps NNN, NNN)"
git push origin main
```

**Do NOT `git add docs/field-notes.json` or `docs/lessons.json`.** The GH Action will regenerate and commit them. Adding them locally creates merge churn.

If `git push` rejects because main moved while you were composing the note, run `git pull --rebase origin main` and push again.

### 8. Verify the action ran (optional but recommended)

If the agent's environment has the `gh` CLI:
```bash
gh run list --limit 2 --json conclusion,name,status
```
Look for `Build journal JSON` to be `success`. If `failure`, surface it to Robert immediately — the JSON didn't regenerate, so the new field note isn't on the live dashboard yet.

If `gh` isn't available, just include a note in your Telegram reply: "pushed; CI will regenerate JSON in ~30s. If you don't see the entry on 100repsproject.com in a minute, the action may have failed."

### 9. Reply to Robert in Telegram

Structured summary:
- Entry written or appended (which file, mood if set)
- Reps tagged
- Lessons reinforced (with proposed updates)
- New lesson candidates (with proposed slug/title/rationale)
- Anything sanitization stripped (so Robert can confirm nothing important got dropped)
- Local validation result: passed / skipped (no python3) / failed (with the error)

## Key invariants

| Rule | Why |
|------|-----|
| Only write to `field-notes/`. Never to `lessons/`. | Lessons are public canon — Robert curates them by hand. |
| Never commit `docs/field-notes.json` or `docs/lessons.json`. | The GH Action is the sole writer. |
| Entries are append-only within a day. | Preserves morning-vs-evening reflection arcs. |
| Frontmatter `date` must equal the filename. | Build step rejects mismatches. |
| Privacy sanitization is non-negotiable. | The journal is on a public domain. |
| Always `git pull` at the start of a session. | Avoid stale-clone surprises. |

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
- `scripts/build_journal.py` — validator + JSON generator (run by CI; optionally by you)
- `docs/field-notes.json`, `docs/lessons.json` — generated by CI; **never hand-edit, never commit**
- `FIELD_NOTES_SPEC.md` — full schema reference
- `skills/universal/rep-update/SKILL.md` — your operating manual (canonical)
- `.github/workflows/build-journal.yml` — the action that regenerates JSONs

## What to do RIGHT NOW if you have a pending unpushed field-note

If you're reading this rev because Robert handed it to you after a previous run got stuck:

1. `cd ~/100reps && git pull --ff-only origin main` (the branch is now merged — you'll see all the journal infrastructure land).
2. If your previous commit added `docs/field-notes.json` or `docs/lessons.json`, amend it to remove those (`git rm --cached docs/field-notes.json docs/lessons.json && git commit --amend --no-edit`). If it only added the markdown, you're already good.
3. `git push origin main`. The action will regenerate the JSONs.
4. Verify on 100repsproject.com that the field note appears in the left panel.
