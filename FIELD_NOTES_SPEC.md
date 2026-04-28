# Field Notes & Lessons Specification

This file documents the schemas and rules for `field-notes/` and `lessons/`. These directories drive the journal surface of the public dashboard at 100repsproject.com. Same rule as `reps.yaml`: malformed files break the live site. Validate before committing.

---

## File: `field-notes/YYYY-MM-DD.md`

One file per calendar day. Authored by Robert's local Telegram agent (extension of the `rep-update` skill). May be re-written same-day in append mode (see "Same-day append" below).

### Frontmatter (required)

```yaml
---
date: 2026-04-26
reps: [11, 14]
tags: [distribution, cold-outreach]
mood: stuck
---
```

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| `date` | YYYY-MM-DD | yes | Must match the filename |
| `reps` | array of int | yes | Rep ids referenced. May be `[]` |
| `tags` | array of string | yes | Lowercase, hyphen-separated. May be `[]` |
| `mood` | string | no | One word. Free-form |

### Body

Markdown. Wikilinks `[[rep:NNN]]` and `[[lesson:slug]]` are post-processed into anchor tags by the build step. Other markdown features (headings, lists, code blocks, links) render as expected. Raw HTML is stripped by the build step's bleach pass.

### Same-day append

If a file exists for today and the agent runs again, the agent appends below the existing body separated by `---` and a level-2 heading timestamp (e.g., `## 2026-04-26 19:42`). Frontmatter is preserved as-is. Never overwrite.

### Privacy

Same rules as `next_step` and `blocker` in `REPS_YAML_SPEC.md`:

- No personal names (first + last)
- No email addresses
- No phone numbers
- No private internal references

The agent applies sanitization before writing the file.

---

## File: `lessons/<slug>.md`

Curated, named insights. **Robert is the sole author.** The agent never writes to `lessons/` — it only suggests new lessons or updates in its Telegram reply.

### Frontmatter (required)

```yaml
---
slug: distribution-beats-craft
title: Distribution Beats Craft for Physical-Product Reps
reps: [9, 11, 14]
tags: [distribution]
first_seen: 2026-03-12
last_updated: 2026-04-26
---
```

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| `slug` | string | yes | Must match the filename (without `.md`) |
| `title` | string | yes | Title-case, human-readable |
| `reps` | array of int | yes | Rep ids the lesson was learned from |
| `tags` | array of string | yes | May be `[]` |
| `first_seen` | YYYY-MM-DD | yes | First time this insight surfaced |
| `last_updated` | YYYY-MM-DD | yes | Update on every edit |

### Body

Markdown. Same wikilink support as field notes. Same bleach sanitization.

### Rules

- Filename slug is the canonical identifier.
- A lesson, once added, should not be deleted; if the insight changes, edit the body and bump `last_updated`.
- No `_pending/` directory — every file under `lessons/` is published.

---

## Build pipeline

`scripts/build_journal.py` walks both directories on push (via `.github/workflows/build-journal.yml`) and emits `docs/field-notes.json` and `docs/lessons.json` consumed by the dashboard.

The build step renders markdown → HTML → bleach-sanitized HTML. Allowlist: paragraphs, headings, lists, emphasis, code, blockquotes, anchors with limited href schemes (http, https, mailto, fragment), and the dashboard's wikilink classes/data attributes.

### Validation

Before pushing, run locally:
```bash
python3 scripts/build_journal.py
python3 -c "import json; json.load(open('docs/field-notes.json')); json.load(open('docs/lessons.json')); print('VALID')"
```

A broken markdown or JSON file takes the journal panel offline.