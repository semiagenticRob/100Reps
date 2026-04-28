# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

Tracking system for the 100 Reps Project (100 product launches). It is **not** a conventional application — it is a data file plus a static dashboard that renders it.

- `reps.yaml` — **single source of truth**. Drives the public dashboard at 100repsproject.com.
- `docs/index.html` — single-file vanilla-JS dashboard (no front-end build) served via GitHub Pages. Fetches `docs/reps.yaml` at runtime via `js-yaml`, enriches each rep with GitHub commit history, and renders a left-side journal panel from `docs/field-notes.json`.
- `docs/reps.yaml` — a copy of the root `reps.yaml`, auto-synced by `.github/workflows/sync-reps-yaml.yml` on every push to `main` that changes `reps.yaml`. **Do not hand-edit `docs/reps.yaml`** — edit the root file and let CI sync it.
- `reps/NNN-name.md` — companion human-readable summary per rep. Must stay in sync with `reps.yaml`.
- `field-notes/YYYY-MM-DD.md` — daily public reflection entries (see "Field Notes & Lessons" below).
- `lessons/<slug>.md` — curated insights distilled from field notes (see "Field Notes & Lessons" below).
- `README.md` — hand-maintained public index of projects by status. Update when reps change status.

## Commands

```bash
npm run dev      # Serves docs/ on http://localhost:3000 (http-server) — preview the dashboard
npx js-yaml reps.yaml > /dev/null    # Validate YAML syntax — REQUIRED before committing reps.yaml
```

Stronger validation (also checks `meta.total` matches reps count):

```bash
python3 -c "import yaml; d=yaml.safe_load(open('reps.yaml')); assert len(d['reps'])==d['meta']['total']; print('VALID')"
```

Journal pipeline (field-notes/lessons → JSON consumed by the dashboard):

```bash
python3 scripts/build_journal.py                # regenerate docs/field-notes.json and docs/lessons.json
python3 -m unittest discover tests -v           # run the build-script tests
```

There is no front-end build or lint suite — only the Python tests above for the journal pipeline.

## Editing `reps.yaml` — critical rules

**A syntax error here takes the live dashboard offline.** The full spec is in `REPS_YAML_SPEC.md` — read it before any non-trivial edit. Key rules that bite:

- Field order is fixed: `id, name, status, pita, summary, next_step, due, blocker, last_action, repo` then optional `links`, `timeline`. Maintain this order.
- `status` must be exactly one of (lowercase): `idea | assessed | building | live | pmf | dead`. Anything else breaks dashboard filters.
- `next_step` and `blocker` are **rendered publicly**. Never put personal names (first + last), emails, phone numbers, or private contact info in them. A sanitizer exists but do not rely on it.
- `last_action` must be updated to today's date on **every** change to a rep.
- Dates are bare `YYYY-MM-DD` (no quotes, no datetime). Nulls are literal `null` (not `~`, not empty string, not omitted).
- `repo` is `owner/repo`, not a full URL. `links` contains only public-facing URLs (`website`, `app_store`, `sales`) — never GitHub URLs.
- Removing a rep: set `status: dead`, do not delete the entry. IDs are never reused or reassigned.
- When adding a rep: append at end, `id = max + 1`, bump `meta.total`.
- Omit empty `links` / `timeline` blocks entirely — never `links: {}` or `timeline: []`.

## When a rep changes state

Three files must move together. The `rep-update` skill at `skills/universal/rep-update/SKILL.md` is the canonical checklist — follow it. In brief:

1. **`reps.yaml`** — update only the changed fields + bump `last_action`.
2. **`reps/NNN-name.md`** — mirror status/next-step/timeline changes. Status line is Title Case; title uses an em dash: `# Rep NNN — Name`. See `REPS_YAML_SPEC.md` §"Rep Markdown Files" for the full template.
3. **Vault Main Note** at `~/second-brain/RW Vault/6 - Main Notes/<Rep Name>.md` — append a dated entry (append-only; do not read before appending).
4. **`README.md`** — update the status tables if a rep moved between sections.

Validate YAML before committing. Commit message convention (see recent log): `Rep NNN <Name>: <what changed>, next_step updated`.

## Field Notes & Lessons (the journal)

In addition to `reps.yaml`, the repo carries a public reflection journal rendered on the dashboard:

- **`field-notes/YYYY-MM-DD.md`** — daily entries written by Robert's local Telegram agent (extension of `rep-update`). Append-only within a day. Renders in a left-side panel on the dashboard.
- **`lessons/<slug>.md`** — curated insights Robert hand-writes when patterns crystallize. The agent NEVER writes here. Renders on `docs/lessons.html`.
- **Schemas and rules:** `FIELD_NOTES_SPEC.md`. Same privacy bar as `next_step`/`blocker` — public-facing, sanitized.
- **Build pipeline:** `scripts/build_journal.py` walks `field-notes/` and `lessons/`, renders markdown to bleach-sanitized HTML, and emits `docs/field-notes.json` + `docs/lessons.json`. The GH Action `.github/workflows/build-journal.yml` runs it on push.
- **Local validation:** before pushing, run `python3 scripts/build_journal.py` and verify both JSONs are valid.
- **Briefing for the local agent:** `AGENT_BRIEFING.md` summarizes the field-notes pipeline; the canonical operating manual is `skills/universal/rep-update/SKILL.md`.

### Adding journal content

- **Add a field note**: write `field-notes/YYYY-MM-DD.md` with frontmatter (`date`, `reps`, `tags`, optional `mood`) and a markdown body. Run `python3 scripts/build_journal.py`. Verify locally. Commit + push.
- **Add a lesson**: write `lessons/<slug>.md` with frontmatter (`slug`, `title`, `reps`, `tags`, `first_seen`, `last_updated`) and a body. Same build/validate/push flow.
