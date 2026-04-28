# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

The 100 Reps Project dashboard. A static GitHub Pages site at **100repsproject.com** that renders a public progress tracker over a YAML-driven catalog of product launches.

There is **no build system, no package manager, no tests** — `docs/index.html` is a single 900-line vanilla HTML/CSS/JS file that fetches `docs/reps.yaml` at runtime and renders it client-side.

## Source of truth and the YAML→docs sync

- **`reps.yaml`** at the repo root is the canonical data file. Edit this, never `docs/reps.yaml` directly.
- **`docs/reps.yaml`** is a published mirror. The `.github/workflows/sync-reps-yaml.yml` GitHub Action automatically copies `reps.yaml` → `docs/reps.yaml` on every push to `main` that touches `reps.yaml`, then commits the mirror with message `sync reps.yaml to docs/`. Do not hand-edit `docs/reps.yaml` — the action will overwrite it.
- A malformed `reps.yaml` takes the live dashboard offline. **Always validate before committing**:
  ```bash
  python3 -c "import yaml; d=yaml.safe_load(open('reps.yaml')); assert len(d['reps'])==d['meta']['total']; print('VALID')"
  # or
  npx js-yaml reps.yaml > /dev/null
  ```

## reps.yaml schema rules (load-bearing)

The full spec is in **`REPS_YAML_SPEC.md`** — read it before editing `reps.yaml`. Key invariants:

- Top-level keys are exactly `meta` and `reps`. `meta.total` must equal `len(reps)`.
- `id` is sequential, never reused, never reassigned. New reps get `max(id) + 1`.
- `status` MUST be one of (lowercase): `idea | assessed | building | live | pmf | dead`. Anything else breaks dashboard filters/colors.
- `pita` is an integer 1-10 (operational lift index, drives color-coded badges).
- `next_step` and `blocker` render publicly — never put personal names, emails, phone numbers, or private references there.
- `last_action` (YYYY-MM-DD) must be updated on every change to a rep.
- `repo` is `owner/repo`, never a full URL. `links` only holds `website`/`app_store`/`sales` — never GitHub URLs (the `repo` field handles that).
- Maintain field order from the schema; 2-space indent; bare `YYYY-MM-DD` dates; literal `null` (not `~`, not empty); one blank line between rep entries, none within.
- Removing a rep means setting `status: dead`, not deleting the entry. Dead reps stay in history.

## Companion markdown files (`reps/NNN-name.md`)

Each rep has a human-readable summary at `reps/NNN-name.md` (zero-padded id, lowercase-hyphenated name). When `reps.yaml` changes for a rep, update its markdown file to match (status line, next steps, milestones). These files are summary cards — detailed planning, specs, and checklists belong in the rep's own dedicated repo, not here.

Required structure documented in `REPS_YAML_SPEC.md` §"Rep Markdown Files".

## Dashboard architecture (`docs/index.html`)

Single self-contained file. Loads `js-yaml` from CDN, fetches `./reps.yaml` (the synced mirror), and renders client-side:

- Status filter pills, search, sort buttons, and a table/card view.
- Default sort by status order: `live, pmf, building, assessed, idea, dead` (see recent commits — this ordering is intentional and was changed twice).
- Staleness detection driven by `last_action` (14d → amber border, 30d → red).
- For reps with a `repo` field, the dashboard fetches commit history from the GitHub API and merges it with manual `timeline` entries.

When changing rendering or adding a field, coordinate the schema change in `reps.yaml` + spec + this dashboard together — the dashboard tolerates unknown fields silently, but mismatches between expectations and data cause subtle UI breakage.

## The `rep-update` skill

`skills/universal/rep-update/SKILL.md` documents the operational protocol used by Robert's external workflow (Telegram updates, brain dumps, vault sync). It enforces a multi-write checklist: `reps.yaml` + `reps/NNN-name.md` + an external Obsidian vault Main Note at `~/second-brain/RW Vault/6 - Main Notes/`. The vault path is outside this repo — only the first two writes are in-tree.

## Common workflows

- **Add a rep**: append to `reps.yaml` with `id = max+1`, increment `meta.total`, create `reps/NNN-name.md`, validate, commit. The Action syncs `docs/reps.yaml`.
- **Update a rep**: edit fields in `reps.yaml` (always bump `last_action`), update the matching `reps/NNN-name.md`, validate, commit.
- **Preview the dashboard locally**: `cd docs && python3 -m http.server 8000` then open `http://localhost:8000`. The page fetches `./reps.yaml` relatively, so serving from `docs/` is required.
