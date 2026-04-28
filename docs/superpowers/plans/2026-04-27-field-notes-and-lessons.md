# Field Notes & Lessons Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a build-in-public reflection journal (Field Notes) and curated Lessons library to the 100 Reps dashboard, sourced from markdown files, generated to JSON by a Python build step, and rendered as a left side panel on the existing dashboard plus a separate lessons page.

**Architecture:** Markdown files at repo root (`field-notes/YYYY-MM-DD.md`, `lessons/<slug>.md`) are source-of-truth. A Python build script (`scripts/build_journal.py`) parses frontmatter, renders body markdown to HTML, sanitizes the HTML through a strict tag allowlist (bleach), and emits `docs/field-notes.json` and `docs/lessons.json`. A GitHub Action runs the script on push. The existing single-file dashboard `docs/index.html` is extended with a left-side panel that fetches the JSON and renders a feed; a new `docs/lessons.html` renders the curated library. The dashboard is purely client-side; no JavaScript build step.

**Tech Stack:** Python 3.11+ (`pyyaml`, `markdown`, `bleach`), Python stdlib `unittest` for tests, vanilla JS / CSS for dashboard, GitHub Actions for CI build.

**Spec:** `docs/superpowers/specs/2026-04-27-field-notes-and-lessons-design.md`

**Security model:** All HTML in `docs/*.json` is produced by the build step from markdown Robert authors. Even so, the build step runs every rendered HTML body through `bleach.clean` with an explicit tag/attribute allowlist before serialization. This means the dashboard JS can safely insert journal HTML via `innerHTML` — the JSON content is guaranteed not to contain `<script>`, inline event handlers, or any tag outside the allowlist. The XSS surface collapses to "is the build step's allowlist correct?" which is testable.

**Naming note:** The design spec calls the script `scripts/build-journal.py` (hyphenated). For Python importability in tests we use `scripts/build_journal.py` (underscored). Module-import friendliness wins; the GH Action references the underscored name.

---

## Task 1: Schema spec document

**Files:**
- Create: `FIELD_NOTES_SPEC.md`

- [ ] **Step 1: Create the spec document**

Create `FIELD_NOTES_SPEC.md` with this content:

```markdown
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
```

- [ ] **Step 2: Commit**

```bash
git add FIELD_NOTES_SPEC.md
git commit -m "docs: add FIELD_NOTES_SPEC.md schema and rules"
```

---

## Task 2: Project Python setup (deps + test scaffolding)

**Files:**
- Create: `requirements.txt`
- Create: `tests/__init__.py`
- Create: `tests/test_build_journal.py` (smoke stub)
- Modify: `.gitignore`

- [ ] **Step 1: Create `requirements.txt`**

```
pyyaml>=6.0
markdown>=3.5
bleach>=6.0
```

- [ ] **Step 2: Install deps locally**

Run:
```bash
pip3 install -r requirements.txt
```

Expected: success — `pyyaml`, `markdown`, and `bleach` installed (or "already satisfied").

- [ ] **Step 3: Create test scaffolding**

Create `tests/__init__.py` (empty file).

Create `tests/test_build_journal.py`:

```python
import unittest


class TestBuildJournal(unittest.TestCase):
    """Tests for scripts/build_journal.py — added in subsequent tasks."""

    def test_smoke(self):
        self.assertTrue(True)


if __name__ == '__main__':
    unittest.main()
```

- [ ] **Step 4: Run smoke test**

Run:
```bash
python3 -m unittest tests.test_build_journal -v
```

Expected: `test_smoke` PASSES, `Ran 1 test`, `OK`.

- [ ] **Step 5: Update `.gitignore`**

Add these lines to `.gitignore` (create the file if it doesn't exist):

```
__pycache__/
*.pyc
.pytest_cache/
```

- [ ] **Step 6: Commit**

```bash
git add requirements.txt tests/__init__.py tests/test_build_journal.py .gitignore
git commit -m "chore: add Python deps and unittest scaffolding for build script"
```

---

## Task 3: Build script — frontmatter parser (TDD)

**Files:**
- Create: `scripts/__init__.py` (empty)
- Create: `scripts/build_journal.py`
- Modify: `tests/test_build_journal.py`

- [ ] **Step 1: Write failing tests for `parse_frontmatter`**

Replace the contents of `tests/test_build_journal.py` with:

```python
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / 'scripts'))
import build_journal


class TestParseFrontmatter(unittest.TestCase):

    def test_parses_field_note_frontmatter(self):
        raw = (
            "---\n"
            "date: 2026-04-26\n"
            "reps: [11, 14]\n"
            "tags: [distribution, cold-outreach]\n"
            "mood: stuck\n"
            "---\n"
            "Body content here.\n"
        )
        meta, body = build_journal.parse_frontmatter(raw)
        self.assertEqual(meta['date'], '2026-04-26')
        self.assertEqual(meta['reps'], [11, 14])
        self.assertEqual(meta['tags'], ['distribution', 'cold-outreach'])
        self.assertEqual(meta['mood'], 'stuck')
        self.assertEqual(body.strip(), 'Body content here.')

    def test_parses_lesson_frontmatter(self):
        raw = (
            "---\n"
            "slug: distribution-beats-craft\n"
            "title: Distribution Beats Craft\n"
            "reps: [9, 11, 14]\n"
            "tags: [distribution]\n"
            "first_seen: 2026-03-12\n"
            "last_updated: 2026-04-26\n"
            "---\n"
            "Lesson body.\n"
        )
        meta, body = build_journal.parse_frontmatter(raw)
        self.assertEqual(meta['slug'], 'distribution-beats-craft')
        self.assertEqual(meta['title'], 'Distribution Beats Craft')
        self.assertEqual(meta['reps'], [9, 11, 14])

    def test_raises_when_no_frontmatter(self):
        with self.assertRaises(ValueError):
            build_journal.parse_frontmatter("Body without frontmatter.\n")

    def test_raises_when_unclosed_frontmatter(self):
        with self.assertRaises(ValueError):
            build_journal.parse_frontmatter("---\ndate: 2026-04-26\nBody\n")

    def test_dates_normalized_to_iso_strings(self):
        # PyYAML auto-parses YYYY-MM-DD as a date object. We want strings.
        raw = "---\ndate: 2026-04-26\nreps: []\ntags: []\n---\nBody\n"
        meta, _ = build_journal.parse_frontmatter(raw)
        self.assertIsInstance(meta['date'], str)
        self.assertEqual(meta['date'], '2026-04-26')


if __name__ == '__main__':
    unittest.main()
```

- [ ] **Step 2: Verify tests fail**

Run:
```bash
python3 -m unittest tests.test_build_journal -v
```

Expected: ImportError or ModuleNotFoundError for `build_journal` — file doesn't exist yet.

- [ ] **Step 3: Create `scripts/__init__.py`**

Empty file.

- [ ] **Step 4: Implement `parse_frontmatter`**

Create `scripts/build_journal.py`:

```python
"""Build script for the 100 Reps Field Notes & Lessons journal.

Walks `field-notes/` and `lessons/` at the repo root, parses each markdown
file (frontmatter + body), renders body markdown to HTML, sanitizes the
HTML through a strict allowlist, and writes `docs/field-notes.json` and
`docs/lessons.json`.
"""
from __future__ import annotations

import datetime as _dt
from typing import Any

import yaml


def parse_frontmatter(raw: str) -> tuple[dict[str, Any], str]:
    """Split a markdown file into (frontmatter dict, body string).

    Frontmatter is YAML between two `---` lines at the very top.
    Date values (YYYY-MM-DD) are normalized to ISO-format strings so
    downstream JSON serialization is straightforward.
    """
    if not raw.startswith('---\n') and not raw.startswith('---\r\n'):
        raise ValueError('file must start with `---` frontmatter')

    lines = raw.splitlines(keepends=True)
    end_idx = None
    for i in range(1, len(lines)):
        if lines[i].rstrip('\r\n') == '---':
            end_idx = i
            break
    if end_idx is None:
        raise ValueError('frontmatter is not closed with a `---` line')

    fm_text = ''.join(lines[1:end_idx])
    body = ''.join(lines[end_idx + 1:])
    meta = yaml.safe_load(fm_text) or {}

    for key, val in list(meta.items()):
        if isinstance(val, _dt.datetime):
            meta[key] = val.isoformat()
        elif isinstance(val, _dt.date):
            meta[key] = val.strftime('%Y-%m-%d')

    return meta, body
```

- [ ] **Step 5: Run tests**

Run:
```bash
python3 -m unittest tests.test_build_journal -v
```

Expected: 5 tests, all PASS.

- [ ] **Step 6: Commit**

```bash
git add scripts/__init__.py scripts/build_journal.py tests/test_build_journal.py
git commit -m "feat(build): add parse_frontmatter for field-notes and lessons"
```

---

## Task 4: Build script — markdown rendering, sanitization, preview (TDD)

**Files:**
- Modify: `scripts/build_journal.py`
- Modify: `tests/test_build_journal.py`

- [ ] **Step 1: Append failing tests for `render_body` and `make_preview`**

Add to `tests/test_build_journal.py` (above the `if __name__` line):

```python
class TestRenderBody(unittest.TestCase):

    def test_renders_paragraphs(self):
        html = build_journal.render_body("First paragraph.\n\nSecond paragraph.\n")
        self.assertIn('<p>First paragraph.</p>', html)
        self.assertIn('<p>Second paragraph.</p>', html)

    def test_renders_lists(self):
        html = build_journal.render_body("- one\n- two\n")
        self.assertIn('<li>one</li>', html)
        self.assertIn('<li>two</li>', html)

    def test_rewrites_rep_wikilinks(self):
        html = build_journal.render_body("See [[rep:011]] for context.\n")
        self.assertIn('class="wl-rep"', html)
        self.assertIn('data-rep-id="11"', html)
        self.assertIn('>011<', html)

    def test_rewrites_lesson_wikilinks(self):
        html = build_journal.render_body("Echoes [[lesson:distribution-beats-craft]].\n")
        self.assertIn('class="wl-lesson"', html)
        self.assertIn('href="lessons.html#distribution-beats-craft"', html)

    def test_sanitization_strips_script_tags(self):
        html = build_journal.render_body("Hello <script>alert(1)</script> world.\n")
        self.assertNotIn('<script', html)
        self.assertNotIn('alert', html)

    def test_sanitization_strips_inline_event_handlers(self):
        # raw HTML in markdown
        html = build_journal.render_body('<a href="x" onclick="evil()">link</a>\n')
        self.assertNotIn('onclick', html)

    def test_sanitization_strips_dangerous_href_schemes(self):
        html = build_journal.render_body("[bad](javascript:alert(1))\n")
        self.assertNotIn('javascript:', html)

    def test_sanitization_preserves_safe_anchors(self):
        html = build_journal.render_body("[ok](https://example.com)\n")
        self.assertIn('href="https://example.com"', html)


class TestMakePreview(unittest.TestCase):

    def test_returns_first_paragraph_stripped_of_markdown(self):
        body = "First **bold** sentence about [a thing](http://x).\n\nSecond paragraph.\n"
        preview = build_journal.make_preview(body)
        self.assertEqual(preview, 'First bold sentence about a thing.')

    def test_truncates_long_first_paragraph_with_ellipsis(self):
        body = ('a' * 200) + '\n\nNext.\n'
        preview = build_journal.make_preview(body)
        self.assertTrue(preview.endswith('…'))
        self.assertLessEqual(len(preview), 141)

    def test_empty_body_returns_empty_string(self):
        self.assertEqual(build_journal.make_preview(''), '')
        self.assertEqual(build_journal.make_preview('\n\n'), '')
```

- [ ] **Step 2: Verify tests fail**

Run:
```bash
python3 -m unittest tests.test_build_journal -v
```

Expected: new tests fail with AttributeError (`render_body` / `make_preview` don't exist yet).

- [ ] **Step 3: Implement `render_body` and `make_preview`**

Append to `scripts/build_journal.py`:

```python
import re

import bleach
import markdown as _markdown

PREVIEW_MAX_CHARS = 140

_REP_WIKILINK = re.compile(r'\[\[rep:(\d+)\]\]')
_LESSON_WIKILINK = re.compile(r'\[\[lesson:([a-z0-9-]+)\]\]')

# Allowlist for bleach. Only these tags survive sanitization.
_ALLOWED_TAGS = [
    'a', 'p', 'br', 'em', 'strong', 'code', 'pre',
    'ul', 'ol', 'li', 'blockquote',
    'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
    'hr', 'span',
]
_ALLOWED_ATTRS = {
    'a': ['href', 'class', 'data-rep-id'],
    'span': ['class'],
    'code': ['class'],
    'pre': ['class'],
}
_ALLOWED_PROTOCOLS = ['http', 'https', 'mailto']


def _rewrite_wikilinks(text: str) -> str:
    """Rewrite [[rep:N]] and [[lesson:slug]] tokens to HTML anchors.

    Runs BEFORE markdown rendering so the resulting <a> tags pass through
    untouched. Anchors carry `class` and `data-` attributes the dashboard
    JS uses to wire interactivity.
    """

    def rep_sub(m: re.Match) -> str:
        rep_id = int(m.group(1))
        display = f'{rep_id:03d}'
        return f'<a class="wl-rep" data-rep-id="{rep_id}" href="#rep-{rep_id}">{display}</a>'

    def lesson_sub(m: re.Match) -> str:
        slug = m.group(1)
        return f'<a class="wl-lesson" href="lessons.html#{slug}">{slug}</a>'

    text = _REP_WIKILINK.sub(rep_sub, text)
    text = _LESSON_WIKILINK.sub(lesson_sub, text)
    return text


def render_body(body: str) -> str:
    """Render markdown to HTML, then sanitize through a strict allowlist.

    The sanitization pass ensures the resulting HTML contains only
    allowlisted tags and attributes. The dashboard JS can safely insert
    this HTML via innerHTML — no script tags, no inline event handlers,
    no dangerous href schemes survive this pipeline.
    """
    pre = _rewrite_wikilinks(body)
    raw_html = _markdown.markdown(pre, extensions=['fenced_code'])
    return bleach.clean(
        raw_html,
        tags=_ALLOWED_TAGS,
        attributes=_ALLOWED_ATTRS,
        protocols=_ALLOWED_PROTOCOLS,
        strip=True,
    )


_INLINE_MD = re.compile(r'(\*\*|__|\*|_|`)')
_LINK_MD = re.compile(r'\[([^\]]+)\]\([^)]+\)')


def make_preview(body: str) -> str:
    """First paragraph, markdown-stripped, max 140 chars + ellipsis if longer."""
    if not body or not body.strip():
        return ''
    first_para = body.strip().split('\n\n', 1)[0]
    stripped = _LINK_MD.sub(r'\1', first_para)
    stripped = _INLINE_MD.sub('', stripped)
    stripped = re.sub(r'\s+', ' ', stripped).strip()
    if len(stripped) > PREVIEW_MAX_CHARS:
        return stripped[:PREVIEW_MAX_CHARS] + '…'
    return stripped
```

- [ ] **Step 4: Run tests**

Run:
```bash
python3 -m unittest tests.test_build_journal -v
```

Expected: 16 tests, all PASS.

- [ ] **Step 5: Commit**

```bash
git add scripts/build_journal.py tests/test_build_journal.py
git commit -m "feat(build): render markdown to sanitized HTML, generate preview"
```

---

## Task 5: Build script — directory walker, JSON emitter, CLI (TDD)

**Files:**
- Modify: `scripts/build_journal.py`
- Modify: `tests/test_build_journal.py`

- [ ] **Step 1: Append failing end-to-end tests**

Add to `tests/test_build_journal.py`:

```python
import json
import shutil
import tempfile
from pathlib import Path


class TestBuildEndToEnd(unittest.TestCase):

    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        (self.tmp / 'field-notes').mkdir()
        (self.tmp / 'lessons').mkdir()
        (self.tmp / 'docs').mkdir()

    def tearDown(self):
        shutil.rmtree(self.tmp)

    def _write(self, rel: str, content: str) -> None:
        (self.tmp / rel).write_text(content)

    def test_emits_field_notes_json_sorted_newest_first(self):
        self._write('field-notes/2026-04-25.md',
            "---\ndate: 2026-04-25\nreps: [3]\ntags: [hardware]\n---\nOlder day.\n")
        self._write('field-notes/2026-04-26.md',
            "---\ndate: 2026-04-26\nreps: [11]\ntags: [distribution]\n---\nNewer day.\n")
        build_journal.build(repo_root=self.tmp)
        data = json.loads((self.tmp / 'docs/field-notes.json').read_text())
        self.assertEqual(len(data['entries']), 2)
        self.assertEqual(data['entries'][0]['date'], '2026-04-26')
        self.assertEqual(data['entries'][1]['date'], '2026-04-25')
        self.assertIn('<p>Newer day.</p>', data['entries'][0]['html'])
        self.assertEqual(data['entries'][0]['preview'], 'Newer day.')
        self.assertEqual(data['entries'][0]['reps'], [11])
        self.assertEqual(data['entries'][0]['tags'], ['distribution'])

    def test_emits_lessons_json_sorted_by_last_updated_desc(self):
        self._write('lessons/old.md',
            "---\nslug: old\ntitle: Old\nreps: [1]\ntags: []\n"
            "first_seen: 2026-01-01\nlast_updated: 2026-01-01\n---\nOld.\n")
        self._write('lessons/new.md',
            "---\nslug: new\ntitle: New\nreps: [2]\ntags: []\n"
            "first_seen: 2026-04-01\nlast_updated: 2026-04-26\n---\nNew.\n")
        build_journal.build(repo_root=self.tmp)
        data = json.loads((self.tmp / 'docs/lessons.json').read_text())
        self.assertEqual(len(data['lessons']), 2)
        self.assertEqual(data['lessons'][0]['slug'], 'new')
        self.assertEqual(data['lessons'][1]['slug'], 'old')

    def test_skips_files_without_frontmatter_with_clear_error(self):
        self._write('field-notes/2026-04-26.md', 'No frontmatter at all.\n')
        with self.assertRaises(ValueError) as ctx:
            build_journal.build(repo_root=self.tmp)
        self.assertIn('2026-04-26.md', str(ctx.exception))

    def test_filename_must_match_field_note_date(self):
        self._write('field-notes/2026-04-26.md',
            "---\ndate: 2026-04-25\nreps: []\ntags: []\n---\nMismatch.\n")
        with self.assertRaises(ValueError) as ctx:
            build_journal.build(repo_root=self.tmp)
        self.assertIn('filename', str(ctx.exception).lower())

    def test_lesson_filename_must_match_slug(self):
        self._write('lessons/wrong-name.md',
            "---\nslug: actual-slug\ntitle: T\nreps: []\ntags: []\n"
            "first_seen: 2026-01-01\nlast_updated: 2026-01-01\n---\nBody.\n")
        with self.assertRaises(ValueError) as ctx:
            build_journal.build(repo_root=self.tmp)
        self.assertIn('slug', str(ctx.exception).lower())

    def test_empty_dirs_emit_empty_arrays(self):
        build_journal.build(repo_root=self.tmp)
        fn = json.loads((self.tmp / 'docs/field-notes.json').read_text())
        ls = json.loads((self.tmp / 'docs/lessons.json').read_text())
        self.assertEqual(fn['entries'], [])
        self.assertEqual(ls['lessons'], [])
```

- [ ] **Step 2: Verify tests fail**

Run:
```bash
python3 -m unittest tests.test_build_journal -v
```

Expected: 6 new tests fail with AttributeError (`build` does not exist).

- [ ] **Step 3: Implement `build()`, loaders, and CLI**

Append to `scripts/build_journal.py`:

```python
import json
import sys
from pathlib import Path


REQUIRED_FIELD_NOTE_KEYS = {'date', 'reps', 'tags'}
REQUIRED_LESSON_KEYS = {'slug', 'title', 'reps', 'tags', 'first_seen', 'last_updated'}


def _load_field_note(path: Path) -> dict[str, Any]:
    raw = path.read_text()
    try:
        meta, body = parse_frontmatter(raw)
    except ValueError as exc:
        raise ValueError(f'{path.name}: {exc}') from exc
    missing = REQUIRED_FIELD_NOTE_KEYS - set(meta)
    if missing:
        raise ValueError(f'{path.name}: missing required keys {sorted(missing)}')
    expected_date = path.stem
    if meta['date'] != expected_date:
        raise ValueError(
            f'{path.name}: filename date does not match frontmatter date '
            f'({expected_date} vs {meta["date"]})'
        )
    return {
        'date': meta['date'],
        'reps': meta.get('reps') or [],
        'tags': meta.get('tags') or [],
        'mood': meta.get('mood'),
        'html': render_body(body),
        'preview': make_preview(body),
    }


def _load_lesson(path: Path) -> dict[str, Any]:
    raw = path.read_text()
    try:
        meta, body = parse_frontmatter(raw)
    except ValueError as exc:
        raise ValueError(f'{path.name}: {exc}') from exc
    missing = REQUIRED_LESSON_KEYS - set(meta)
    if missing:
        raise ValueError(f'{path.name}: missing required keys {sorted(missing)}')
    expected_slug = path.stem
    if meta['slug'] != expected_slug:
        raise ValueError(
            f'{path.name}: filename slug does not match frontmatter slug '
            f'({expected_slug} vs {meta["slug"]})'
        )
    return {
        'slug': meta['slug'],
        'title': meta['title'],
        'reps': meta.get('reps') or [],
        'tags': meta.get('tags') or [],
        'first_seen': meta['first_seen'],
        'last_updated': meta['last_updated'],
        'html': render_body(body),
    }


def build(repo_root: Path | None = None) -> None:
    """Walk field-notes/ and lessons/ and emit docs/*.json."""
    repo_root = Path(repo_root) if repo_root else Path(__file__).resolve().parent.parent

    fn_dir = repo_root / 'field-notes'
    ls_dir = repo_root / 'lessons'
    docs_dir = repo_root / 'docs'
    docs_dir.mkdir(exist_ok=True)

    field_notes: list[dict[str, Any]] = []
    if fn_dir.is_dir():
        for path in sorted(fn_dir.glob('*.md')):
            field_notes.append(_load_field_note(path))
    field_notes.sort(key=lambda e: e['date'], reverse=True)

    lessons: list[dict[str, Any]] = []
    if ls_dir.is_dir():
        for path in sorted(ls_dir.glob('*.md')):
            lessons.append(_load_lesson(path))
    lessons.sort(key=lambda e: e['last_updated'], reverse=True)

    (docs_dir / 'field-notes.json').write_text(
        json.dumps({'entries': field_notes}, indent=2, ensure_ascii=False) + '\n'
    )
    (docs_dir / 'lessons.json').write_text(
        json.dumps({'lessons': lessons}, indent=2, ensure_ascii=False) + '\n'
    )


def main() -> int:
    try:
        build()
    except ValueError as exc:
        print(f'BUILD FAILED: {exc}', file=sys.stderr)
        return 1
    print('OK: wrote docs/field-notes.json and docs/lessons.json')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
```

- [ ] **Step 4: Run all tests**

Run:
```bash
python3 -m unittest tests.test_build_journal -v
```

Expected: 22 tests, all PASS.

- [ ] **Step 5: Commit**

```bash
git add scripts/build_journal.py tests/test_build_journal.py
git commit -m "feat(build): add directory walker, JSON emitter, and CLI"
```

---

## Task 6: Smoke content + first local build

**Files:**
- Create: `field-notes/.gitkeep`
- Create: `field-notes/2026-04-27.md`
- Create: `lessons/.gitkeep`
- Create: `lessons/distribution-beats-craft.md`

- [ ] **Step 1: Create `field-notes/.gitkeep`** (empty file)

- [ ] **Step 2: Create `field-notes/2026-04-27.md`**

```markdown
---
date: 2026-04-27
reps: [11, 14]
tags: [distribution, cold-outreach]
mood: clear
---
First field note. The pattern across [[rep:011]] and [[rep:014]] is the same: I keep building the product and not the distribution. Cold outreach by hand is the only thing that's ever moved a needle.

This realization is the seed of [[lesson:distribution-beats-craft]].
```

- [ ] **Step 3: Create `lessons/.gitkeep`** (empty file)

- [ ] **Step 4: Create `lessons/distribution-beats-craft.md`**

```markdown
---
slug: distribution-beats-craft
title: Distribution Beats Craft for Physical-Product and Personal-Service Reps
reps: [9, 11, 14]
tags: [distribution]
first_seen: 2026-04-27
last_updated: 2026-04-27
---
Across multiple reps, the same failure mode keeps showing up: I build the product carefully and assume distribution will follow from quality. It doesn't. The only motion that has ever moved a needle on these reps is hand-cranked cold outreach — direct DMs, calls, in-person.

The lesson: for any rep where the buyer isn't already in a search-driven funnel (App Store, Google, marketplace), the first 90 days of work should be 70% distribution and 30% product, not the inverse.
```

- [ ] **Step 5: Run the build**

```bash
python3 scripts/build_journal.py
```

Expected: `OK: wrote docs/field-notes.json and docs/lessons.json`. Exit 0.

- [ ] **Step 6: Validate output**

```bash
python3 -c "import json; d=json.load(open('docs/field-notes.json')); print('entries:', len(d['entries'])); print('newest:', d['entries'][0]['date'])"
python3 -c "import json; d=json.load(open('docs/lessons.json')); print('lessons:', len(d['lessons'])); print('newest:', d['lessons'][0]['slug'])"
```

Expected:
```
entries: 1
newest: 2026-04-27
lessons: 1
newest: distribution-beats-craft
```

- [ ] **Step 7: Inspect rendered HTML for wikilinks**

```bash
python3 -c "import json; d=json.load(open('docs/field-notes.json')); print(d['entries'][0]['html'])"
```

Expected output contains `class="wl-rep" data-rep-id="11"` and `class="wl-lesson" href="lessons.html#distribution-beats-craft"`.

- [ ] **Step 8: Commit**

```bash
git add field-notes/ lessons/ docs/field-notes.json docs/lessons.json
git commit -m "feat: add first field note and lesson, generate JSON"
```

---

## Task 7: GitHub Action workflow

**Files:**
- Create: `.github/workflows/build-journal.yml`

- [ ] **Step 1: Create the workflow**

```yaml
name: Build journal JSON

on:
  push:
    branches: [main]
    paths:
      - 'field-notes/**'
      - 'lessons/**'
      - 'scripts/build_journal.py'
      - 'requirements.txt'

permissions:
  contents: write

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: pip install -r requirements.txt

      - name: Run build script
        run: python3 scripts/build_journal.py

      - name: Commit regenerated JSONs if changed
        run: |
          git config user.name "github-actions[bot]"
          git config user.email "github-actions[bot]@users.noreply.github.com"
          git add docs/field-notes.json docs/lessons.json
          git diff --cached --quiet && exit 0
          git commit -m "build: regenerate field-notes.json and lessons.json"
          git push
```

- [ ] **Step 2: Commit**

```bash
git add .github/workflows/build-journal.yml
git commit -m "ci: add build-journal workflow to regenerate journal JSONs on push"
```

> **Defer pushing.** The dashboard UI lands in Tasks 8-12. Pushing now is harmless but premature. Phase B push is in Task 16.

---

## Task 8: Dashboard CSS — left panel layout

**Files:**
- Modify: `docs/index.html` (CSS block, before `</style>` at ~line 169)

- [ ] **Step 1: Add layout CSS**

Open `docs/index.html`. Find the closing `</style>` tag (currently line 169). Insert this CSS *immediately before* `</style>`:

```css

/* ── JOURNAL PANEL ── */
:root{--panel-w:360px;--rail-w:32px}
.app-shell{display:flex;align-items:flex-start;min-height:100vh}
.journal{flex:0 0 var(--panel-w);background:var(--bg2);border-right:1px solid var(--grid);position:sticky;top:0;height:100vh;overflow-y:auto;display:flex;flex-direction:column;transition:flex-basis .25s ease}
.journal.collapsed{flex-basis:var(--rail-w)}
.journal.collapsed .journal-body,.journal.collapsed .journal-head .journal-tabs,.journal.collapsed .journal-head .journal-title{display:none}
.journal-head{padding:16px 14px 8px;border-bottom:1px solid var(--grid);display:flex;align-items:center;gap:8px;flex-wrap:wrap}
.journal-title{color:var(--green);font-size:12px;font-weight:700;letter-spacing:2px;flex:1}
.journal-toggle{background:none;border:1px solid var(--grid);color:var(--green);font-family:var(--font);font-size:11px;padding:2px 6px;cursor:pointer;border-radius:2px}
.journal-toggle:hover{background:var(--bg3)}
.journal-stale-dot{display:inline-block;width:8px;height:8px;border-radius:50%;background:var(--amber);margin-left:4px}
.journal-tabs{display:flex;gap:4px;width:100%}
.journal-tab{padding:3px 8px;font-size:10px;border:1px solid var(--grid);color:var(--dim);background:var(--bg3);border-radius:2px;text-decoration:none;text-transform:uppercase;letter-spacing:1px}
.journal-tab.active{color:var(--green);border-color:var(--green);background:var(--bg)}
.journal-tab:hover{color:var(--text);text-decoration:none}
.journal-body{padding:8px 14px 24px;flex:1}
.journal-empty{color:var(--dim);font-size:11px;padding:14px 0}
.journal-entry{padding:14px 0;border-bottom:1px dashed var(--grid)}
.journal-entry:last-child{border-bottom:0}
.journal-entry-date{color:var(--green);font-size:11px;font-weight:700;letter-spacing:1px;margin-bottom:6px}
.journal-entry-meta{display:flex;flex-wrap:wrap;gap:6px;margin-bottom:8px}
.rep-chip{display:inline-block;padding:1px 6px;font-size:10px;color:var(--green);background:var(--bg3);border:1px solid var(--grid);border-radius:2px;cursor:pointer;font-family:var(--font)}
.rep-chip:hover{border-color:var(--green);background:var(--bg)}
.tag-chip{display:inline-block;padding:1px 6px;font-size:10px;color:var(--blue);background:transparent;border:1px solid var(--grid);border-radius:2px}
.journal-entry-body{color:var(--text);font-size:12px;line-height:1.5}
.journal-entry-body p{margin-bottom:8px}
.journal-entry-body p:last-child{margin-bottom:0}
.journal-entry-preview{color:var(--text);font-size:12px;line-height:1.5;cursor:pointer}
.journal-entry-preview:hover{color:#fff}
.journal-entry .wl-rep{color:var(--green);font-weight:700;text-decoration:none;border-bottom:1px dotted var(--green)}
.journal-entry .wl-lesson{color:var(--magenta);text-decoration:none;border-bottom:1px dotted var(--magenta)}
.journal-rail{display:none;writing-mode:vertical-rl;transform:rotate(180deg);color:var(--dim);font-size:10px;letter-spacing:3px;padding:14px 0;cursor:pointer;user-select:none}
.journal.collapsed .journal-rail{display:block;text-align:center;width:var(--rail-w)}
.journal.collapsed .journal-head{display:none}

.dashboard-col{flex:1;min-width:0}

@media(max-width:900px){
  .app-shell{display:block}
  .journal{position:fixed;top:0;left:0;height:100vh;z-index:50;flex-basis:var(--rail-w);width:var(--rail-w);border-right:1px solid var(--grid)}
  .journal:not(.collapsed){width:min(420px,90vw);flex-basis:auto}
  .journal.collapsed .journal-rail{display:block;height:100vh}
  .dashboard-col{margin-left:var(--rail-w)}
}
```

- [ ] **Step 2: Commit**

```bash
git add docs/index.html
git commit -m "feat(dashboard): add CSS for left-side journal panel"
```

---

## Task 9: Dashboard DOM + JS — render field notes feed

**Files:**
- Modify: `docs/index.html` (body and `<script>` block)

- [ ] **Step 1: Wrap body content in two-column shell**

Open `docs/index.html`. Find this line (currently ~line 173):
```html
<div class="error-banner" id="errorBanner"></div>
```

Insert *before* it (between `<body>` and the error-banner line):
```html

<div class="app-shell">

<aside class="journal" id="journalPanel">
  <div class="journal-rail" id="journalRail">FIELD&nbsp;NOTES</div>
  <div class="journal-head">
    <div class="journal-title">FIELD NOTES <span id="journalStaleDot" class="journal-stale-dot" style="display:none" title="No entry in &gt;3 days"></span></div>
    <button class="journal-toggle" id="journalToggle" title="Collapse panel">&laquo;</button>
    <div class="journal-tabs">
      <a class="journal-tab active" href="#" aria-current="page">Notes</a>
      <a class="journal-tab" href="lessons.html">Lessons &rarr;</a>
    </div>
  </div>
  <div class="journal-body" id="journalBody">
    <div class="journal-empty">Loading…</div>
  </div>
</aside>

<div class="dashboard-col">
```

Then find `<noscript>` (currently ~line 236). Insert *immediately before* it:
```html

</div><!-- /.dashboard-col -->
</div><!-- /.app-shell -->
```

Verify the structure: `<body>` → `<div class="app-shell">` → `<aside class="journal">` + `<div class="dashboard-col">[existing dashboard]</div>` → close shell → `<noscript>...`.

- [ ] **Step 2: Add fetch + render JS**

In `docs/index.html`, locate the `/* ── Init ── */` comment near the bottom (currently ~line 903). Insert this block *immediately before* it:

```javascript

/* ── Journal panel ── */
var FIELD_NOTES_URL = './field-notes.json';
var fieldNotes = [];

function fetchFieldNotes() {
  return fetch(FIELD_NOTES_URL + '?t=' + Date.now())
    .then(function(resp) {
      if (!resp.ok) throw new Error('HTTP ' + resp.status);
      return resp.json();
    })
    .then(function(data) {
      fieldNotes = (data && data.entries) || [];
    })
    .catch(function(err) {
      console.warn('field-notes fetch failed:', err);
      fieldNotes = [];
    });
}

function renderJournal() {
  var $body = document.getElementById('journalBody');
  if (!$body) return;

  var $dot = document.getElementById('journalStaleDot');
  if ($dot) {
    if (fieldNotes.length === 0) {
      $dot.style.display = 'none';
    } else {
      var newestDate = new Date(fieldNotes[0].date);
      var ageDays = Math.floor((new Date() - newestDate) / (1000 * 60 * 60 * 24));
      $dot.style.display = ageDays > 3 ? 'inline-block' : 'none';
    }
  }

  if (fieldNotes.length === 0) {
    $body.innerHTML = '<div class="journal-empty">No field notes yet.</div>';
    return;
  }

  // Build feed via DOM construction so user-facing text is set as textContent.
  // The .html field is bleach-sanitized server-side (see scripts/build_journal.py)
  // so it's safe to assign to innerHTML.
  $body.textContent = '';
  fieldNotes.forEach(function(entry, idx) {
    var isNewest = idx === 0;

    var $entry = document.createElement('div');
    $entry.className = 'journal-entry';
    $entry.dataset.date = entry.date;

    var $date = document.createElement('div');
    $date.className = 'journal-entry-date';
    $date.textContent = entry.date;
    $entry.appendChild($date);

    var $meta = document.createElement('div');
    $meta.className = 'journal-entry-meta';
    (entry.reps || []).forEach(function(rid) {
      var $chip = document.createElement('span');
      $chip.className = 'rep-chip';
      $chip.dataset.repId = String(rid);
      $chip.textContent = String(rid).padStart(3, '0');
      $meta.appendChild($chip);
    });
    (entry.tags || []).forEach(function(t) {
      var $tag = document.createElement('span');
      $tag.className = 'tag-chip';
      $tag.textContent = '#' + t;
      $meta.appendChild($tag);
    });
    $entry.appendChild($meta);

    if (isNewest) {
      var $bodyEl = document.createElement('div');
      $bodyEl.className = 'journal-entry-body';
      // entry.html is bleach-sanitized — safe for innerHTML
      $bodyEl.innerHTML = entry.html;
      $entry.appendChild($bodyEl);
    } else {
      var $prev = document.createElement('div');
      $prev.className = 'journal-entry-preview';
      $prev.dataset.expand = String(idx);
      $prev.textContent = entry.preview || '';
      $entry.appendChild($prev);
    }

    $body.appendChild($entry);
  });

  // Wire rep chips
  $body.querySelectorAll('.rep-chip, a.wl-rep').forEach(function(el) {
    el.addEventListener('click', function(e) {
      e.preventDefault();
      var rid = parseInt(el.dataset.repId);
      if (!isNaN(rid)) scrollToRep(rid);
    });
  });

  // Wire expand-on-click for non-newest previews
  $body.querySelectorAll('.journal-entry-preview').forEach(function(el) {
    el.addEventListener('click', function() {
      var idx = parseInt(el.dataset.expand);
      if (isNaN(idx)) return;
      var entry = fieldNotes[idx];
      if (!entry) return;
      var $bodyEl = document.createElement('div');
      $bodyEl.className = 'journal-entry-body';
      $bodyEl.innerHTML = entry.html; // sanitized server-side
      el.parentNode.replaceChild($bodyEl, el);
      // Bind any newly-revealed rep wikilinks
      $bodyEl.querySelectorAll('a.wl-rep').forEach(function(a) {
        a.addEventListener('click', function(e) {
          e.preventDefault();
          var rid = parseInt(a.dataset.repId);
          if (!isNaN(rid)) scrollToRep(rid);
        });
      });
    });
  });
}
```

- [ ] **Step 3: Wire journal into init**

Find this block (currently ~lines 903-908):

```javascript
/* ── Init ── */
fetchData(false).then(function() {
  render();
  computeLastActions().then(function() { render(); });
  setInterval(refresh, POLL_INTERVAL);
});
```

Replace with:

```javascript
/* ── Init ── */
fetchData(false).then(function() {
  render();
  computeLastActions().then(function() { render(); });
  setInterval(refresh, POLL_INTERVAL);
});
fetchFieldNotes().then(renderJournal);
```

- [ ] **Step 4: Local smoke**

Run:
```bash
cd docs && python3 -m http.server 8000
```

Open `http://localhost:8000`. Confirm:
- Left panel renders with "FIELD NOTES" title
- The 2026-04-27 entry shows fully expanded with date, two rep chips, two tag chips, body text
- Wikilinks render as styled chips (green for rep, magenta for lesson)
- Existing rep table on the right is unaffected

Stop server.

- [ ] **Step 5: Commit**

```bash
git add docs/index.html
git commit -m "feat(dashboard): render field notes feed in left panel"
```

---

## Task 10: Dashboard JS — collapse toggle and rep-chip integration

**Files:**
- Modify: `docs/index.html` (extend journal section from Task 9)

- [ ] **Step 1: Add chrome wiring**

In `docs/index.html`, find the journal panel JS section. Append this code to the end of that section, *before* `/* ── Init ── */`:

```javascript

function wireJournalChrome() {
  var $panel = document.getElementById('journalPanel');
  var $toggle = document.getElementById('journalToggle');
  var $rail = document.getElementById('journalRail');
  if (!$panel) return;

  function setCollapsed(collapsed) {
    $panel.classList.toggle('collapsed', collapsed);
    if ($toggle) {
      $toggle.innerHTML = collapsed ? '&raquo;' : '&laquo;';
      $toggle.title = collapsed ? 'Expand panel' : 'Collapse panel';
    }
    try { localStorage.setItem('journalCollapsed', collapsed ? '1' : '0'); } catch(e) {}
  }

  var stored;
  try { stored = localStorage.getItem('journalCollapsed'); } catch(e) {}
  if (stored === '1') {
    setCollapsed(true);
  } else if (stored === '0') {
    setCollapsed(false);
  } else if (window.matchMedia('(max-width: 900px)').matches) {
    setCollapsed(true);
  }

  if ($toggle) {
    $toggle.addEventListener('click', function() {
      setCollapsed(!$panel.classList.contains('collapsed'));
    });
  }
  if ($rail) {
    $rail.addEventListener('click', function() {
      setCollapsed(false);
    });
  }
}
```

- [ ] **Step 2: Call on init**

Find:
```javascript
fetchFieldNotes().then(renderJournal);
```

Replace with:
```javascript
wireJournalChrome();
fetchFieldNotes().then(renderJournal);
```

- [ ] **Step 3: Local smoke — toggle and responsive**

Serve and open. Confirm:
- Click the `«` button → panel collapses to a vertical rail showing "FIELD NOTES" rotated, dashboard expands
- Click the rail → panel re-expands
- Reload → state persists
- Resize ≤ 900px → panel becomes a fixed left rail with overlay-on-expand

- [ ] **Step 4: Verify rep-chip click integration**

Click a `[011]` chip in the panel. Confirm:
- Rep 011 row in the table expands open
- Page scrolls to bring it into view (handled by existing `scrollToRep`)

- [ ] **Step 5: Commit**

```bash
git add docs/index.html
git commit -m "feat(dashboard): journal panel collapse toggle with persisted state"
```

---

## Task 11: Lessons page (`docs/lessons.html`)

**Files:**
- Create: `docs/lessons.html`

- [ ] **Step 1: Create the file**

Create `docs/lessons.html`:

```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Lessons // 100 REPS</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&display=swap" rel="stylesheet">
<style>
*{margin:0;padding:0;box-sizing:border-box}
:root{
  --bg:#0a0a0a;--bg2:#111;--bg3:#1a1a1a;
  --green:#00ff41;--amber:#ff9900;--red:#ff3333;
  --blue:#4a9eff;--magenta:#ff00ff;--gray:#666;
  --grid:#1a3a1a;--text:#c0c0c0;--dim:#555;
  --font:'JetBrains Mono','Fira Code','Consolas','Courier New',monospace;
}
html,body{background:var(--bg);color:var(--text);font-family:var(--font);font-size:13px;line-height:1.5;min-height:100vh}
a{color:var(--green);text-decoration:none}
a:hover{text-decoration:underline}
.wrap{max-width:760px;margin:0 auto;padding:32px 24px 80px}
.crumb{font-size:11px;color:var(--dim);letter-spacing:2px;margin-bottom:8px;text-transform:uppercase}
.crumb a{color:var(--amber)}
h1{color:var(--green);font-size:22px;font-weight:700;letter-spacing:3px;margin-bottom:6px}
.sub{color:var(--dim);font-size:12px;margin-bottom:32px}
.lesson{padding:24px 0;border-bottom:1px solid var(--grid)}
.lesson:last-child{border-bottom:0}
.lesson-title{color:#fff;font-size:16px;font-weight:700;margin-bottom:8px}
.lesson-meta{display:flex;flex-wrap:wrap;gap:6px;margin-bottom:14px;align-items:center;font-size:11px;color:var(--dim)}
.rep-chip{display:inline-block;padding:1px 6px;font-size:10px;color:var(--green);background:var(--bg3);border:1px solid var(--grid);border-radius:2px;font-family:var(--font)}
.rep-chip a{color:inherit;text-decoration:none}
.tag-chip{display:inline-block;padding:1px 6px;font-size:10px;color:var(--blue);border:1px solid var(--grid);border-radius:2px}
.lesson-dates{margin-left:auto;color:var(--dim);font-size:10px;letter-spacing:1px;text-transform:uppercase}
.lesson-body{color:var(--text);font-size:13px;line-height:1.6}
.lesson-body p{margin-bottom:10px}
.lesson-body p:last-child{margin-bottom:0}
.lesson-body .wl-rep{color:var(--green);font-weight:700;border-bottom:1px dotted var(--green)}
.lesson-body .wl-lesson{color:var(--magenta);border-bottom:1px dotted var(--magenta)}
.empty{color:var(--dim);padding:48px 0;text-align:center}
</style>
</head>
<body>
<div class="wrap">
  <div class="crumb"><a href="index.html">&larr; Dashboard</a></div>
  <h1>LESSONS</h1>
  <div class="sub" id="sub">Loading…</div>
  <div id="list"></div>
</div>

<noscript>
  <div style="padding:40px;color:#ff3333;text-align:center">JavaScript is required to load lessons.</div>
</noscript>

<script>
(function(){
'use strict';

fetch('./lessons.json?t=' + Date.now())
  .then(function(r){ return r.json(); })
  .then(function(data){
    var lessons = (data && data.lessons) || [];
    var $sub = document.getElementById('sub');
    var $list = document.getElementById('list');
    if (lessons.length === 0) {
      $sub.textContent = 'No lessons yet.';
      var $empty = document.createElement('div');
      $empty.className = 'empty';
      $empty.textContent = 'Lessons appear here as patterns crystallize across reps.';
      $list.appendChild($empty);
      return;
    }
    var allReps = {};
    lessons.forEach(function(l){ (l.reps || []).forEach(function(r){ allReps[r] = true; }); });
    var repCount = Object.keys(allReps).length;
    $sub.textContent = lessons.length + ' lesson' + (lessons.length === 1 ? '' : 's') +
      ' across ' + repCount + ' rep' + (repCount === 1 ? '' : 's') + '.';

    // DOM-construction with safe text + sanitized innerHTML for body only.
    lessons.forEach(function(l){
      var $art = document.createElement('article');
      $art.className = 'lesson';
      $art.id = l.slug;

      var $h2 = document.createElement('h2');
      $h2.className = 'lesson-title';
      $h2.textContent = l.title;
      $art.appendChild($h2);

      var $meta = document.createElement('div');
      $meta.className = 'lesson-meta';
      (l.reps || []).forEach(function(rid){
        var $chip = document.createElement('span');
        $chip.className = 'rep-chip';
        var $a = document.createElement('a');
        $a.href = 'index.html#rep-' + rid;
        $a.dataset.repId = String(rid);
        $a.textContent = String(rid).padStart(3, '0');
        $chip.appendChild($a);
        $meta.appendChild($chip);
      });
      (l.tags || []).forEach(function(t){
        var $tag = document.createElement('span');
        $tag.className = 'tag-chip';
        $tag.textContent = '#' + t;
        $meta.appendChild($tag);
      });
      var $dates = document.createElement('span');
      $dates.className = 'lesson-dates';
      $dates.textContent = 'First seen ' + l.first_seen + ' · Updated ' + l.last_updated;
      $meta.appendChild($dates);
      $art.appendChild($meta);

      var $body = document.createElement('div');
      $body.className = 'lesson-body';
      // l.html is bleach-sanitized server-side (see scripts/build_journal.py)
      $body.innerHTML = l.html;
      $art.appendChild($body);

      $list.appendChild($art);
    });
  })
  .catch(function(err){
    console.error('lessons fetch failed:', err);
    document.getElementById('sub').textContent = 'Failed to load lessons.';
  });
})();
</script>
</body>
</html>
```

- [ ] **Step 2: Local smoke**

Serve `cd docs && python3 -m http.server 8000`. Open `http://localhost:8000/lessons.html`. Confirm:
- "LESSONS" header
- Sub: "1 lesson across 3 reps."
- Card with title, three rep chips (009, 011, 014), `#distribution` tag, dates
- Body renders as paragraphs
- "← Dashboard" returns to `index.html`

- [ ] **Step 3: Commit**

```bash
git add docs/lessons.html
git commit -m "feat: add lessons page (docs/lessons.html)"
```

---

## Task 12: Per-rep field-notes section in expanded detail

**Files:**
- Modify: `docs/index.html` (`renderTable` function)

- [ ] **Step 1: Add filtering helper**

In the journal panel JS section, append (above `wireJournalChrome`):

```javascript

function fieldNotesForRep(repId) {
  return fieldNotes.filter(function(e) {
    return (e.reps || []).indexOf(repId) >= 0;
  });
}
```

- [ ] **Step 2: Render notes inside detail expansion**

In `renderTable`, find this block (currently ~lines 514-520):

```javascript
    html += '<div class="detail-section"><div class="detail-label">Timeline</div><div class="timeline-full" id="timeline-'+rep.id+'">';
    if (rep.repo || rep.timeline.length > 0) {
      html += '<div class="timeline-loading">Loading history…</div>';
    } else {
      html += '<div class="timeline-loading">No history available</div>';
    }
    html += '</div></div>';
```

Insert *immediately before* this block:

```javascript
    var repNotes = fieldNotesForRep(rep.id);
    if (repNotes.length > 0) {
      html += '<div class="detail-section"><div class="detail-label">Field Notes ('+repNotes.length+')</div><div class="detail-text">';
      repNotes.slice(0, 5).forEach(function(en) {
        html += '<div style="margin-bottom:6px"><span style="color:var(--green);font-weight:700;font-size:11px">'+esc(en.date)+'</span> <span style="color:var(--text)">'+esc(en.preview || '')+'</span></div>';
      });
      if (repNotes.length > 5) {
        html += '<div style="color:var(--dim);font-size:11px">+ '+(repNotes.length-5)+' older entries</div>';
      }
      html += '</div></div>';
    }
```

(Note: this section uses string concatenation with `esc()` for date and preview values, matching the existing pattern in `renderTable`. Date and preview are plain text per the build script — no HTML — and `esc()` provides defense in depth.)

- [ ] **Step 3: Re-render rep table after field notes load**

Find:
```javascript
fetchFieldNotes().then(renderJournal);
```

Replace with:
```javascript
fetchFieldNotes().then(function() {
  renderJournal();
  if (reps.length > 0) render();
});
```

- [ ] **Step 4: Local smoke**

Serve and open. Click on rep 011 to expand. Confirm:
- Detail panel shows a "Field Notes (1)" subsection
- The 2026-04-27 preview line appears

Click rep 008 (no field notes). Confirm:
- No Field Notes subsection appears

- [ ] **Step 5: Commit**

```bash
git add docs/index.html
git commit -m "feat(dashboard): show per-rep field notes inside expanded detail"
```

---

## Task 13: Extend the rep-update skill with field-notes/lessons protocol

**Files:**
- Modify: `skills/universal/rep-update/SKILL.md`

- [ ] **Step 1: Update frontmatter description**

In `skills/universal/rep-update/SKILL.md`, find the `description:` line in the frontmatter:

```
description: Enforces the two-write checklist for rep state changes. Use this skill whenever a rep's status, blocker, next_step, or any other state field changes — whether from a Telegram update, todo completion, or brain dump containing rep progress. Never update reps.yaml without also updating the vault Main Note.
```

Replace with:

```
description: Enforces the multi-write checklist for rep state changes AND processes daily voice-memo field notes for the public reflection journal. Use this skill whenever a rep's status, blocker, next_step, or any other state field changes — whether from a Telegram update, todo completion, or brain dump — and when Robert sends a daily voice memo intended as a field-note entry.
```

- [ ] **Step 2: Update "When to Use" bullets**

Find the `## When to Use` section. Replace its bullet list with:

```markdown
- Robert reports progress on a rep via Telegram
- A todo prefixed with "Rep NNN" is completed
- Any rep field changes (status, blocker, next_step, last_action, due)
- A brain dump contains rep-level progress or decisions
- **Robert sends a daily voice memo / transcript intended as a field-note reflection** (treat any free-form reflective transcript that mentions one or more reps as a field-note candidate, not a rep update — see the Field Notes section below)
```

- [ ] **Step 3: Add the Field Notes & Lessons section**

*Before* the `## Quick Checklist` section at the end of the file, insert:

```markdown
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
```

- [ ] **Step 4: Commit**

```bash
git add skills/universal/rep-update/SKILL.md
git commit -m "docs(skill): add field-notes/lessons authoring protocol to rep-update"
```

---

## Task 14: Update CLAUDE.md

**Files:**
- Modify: `CLAUDE.md`

- [ ] **Step 1: Add Field Notes & Lessons section**

In `CLAUDE.md`, find the section heading `## The \`rep-update\` skill`. Insert *immediately above* it:

```markdown
## Field Notes & Lessons (the journal)

In addition to `reps.yaml`, the repo carries a public reflection journal:

- **`field-notes/YYYY-MM-DD.md`** — daily entries written by Robert's local Telegram agent (extension of `rep-update`). Append-only within a day. Renders in a left-side panel on the dashboard.
- **`lessons/<slug>.md`** — curated insights Robert hand-writes when patterns crystallize. The agent NEVER writes here. Renders on `docs/lessons.html`.
- **Schemas and rules:** `FIELD_NOTES_SPEC.md`. Same privacy bar as `next_step`/`blocker` — public-facing, sanitized.
- **Build pipeline:** `scripts/build_journal.py` walks `field-notes/` and `lessons/`, renders markdown to bleach-sanitized HTML, and emits `docs/field-notes.json` + `docs/lessons.json`. The GH Action `.github/workflows/build-journal.yml` runs it on push.
- **Local validation:** before pushing, run `python3 scripts/build_journal.py` and verify both JSONs are valid.
- **Tests:** `python3 -m unittest tests.test_build_journal -v`.

```

- [ ] **Step 2: Update Common workflows**

In `CLAUDE.md`, find the `## Common workflows` section. Add to the end of the existing list:

```markdown
- **Add a field note**: write `field-notes/YYYY-MM-DD.md` with frontmatter (`date`, `reps`, `tags`, optional `mood`) and a markdown body. Run `python3 scripts/build_journal.py`. Verify locally at `http://localhost:8000`. Commit + push.
- **Add a lesson**: write `lessons/<slug>.md` with frontmatter (`slug`, `title`, `reps`, `tags`, `first_seen`, `last_updated`) and a body. Same build/validate/push flow.
```

- [ ] **Step 3: Commit**

```bash
git add CLAUDE.md
git commit -m "docs: document field-notes and lessons in CLAUDE.md"
```

---

## Task 15: Final local-verification gate (Phase A from the spec)

**Files:** none modified — verification.

- [ ] **Step 1: Run all unit tests**

```bash
python3 -m unittest discover tests -v
```

Expected: all tests pass.

- [ ] **Step 2: Run the build script**

```bash
python3 scripts/build_journal.py
```

Expected: `OK: wrote docs/field-notes.json and docs/lessons.json`.

- [ ] **Step 3: Validate generated JSON**

```bash
python3 -c "import json; json.load(open('docs/field-notes.json')); json.load(open('docs/lessons.json')); print('VALID')"
```

Expected: `VALID`.

- [ ] **Step 4: Validate `reps.yaml` (no regressions)**

```bash
python3 -c "import yaml; data=yaml.safe_load(open('reps.yaml')); assert len(data['reps'])==data['meta']['total']; print('reps.yaml VALID')"
```

Expected: `reps.yaml VALID`.

- [ ] **Step 5: Serve the dashboard locally and verify visually**

```bash
cd docs && python3 -m http.server 8000
```

Open `http://localhost:8000`. Confirm:
- Left panel: "FIELD NOTES" title, the 2026-04-27 entry expanded with body, rep chips clickable, tag chips visible
- Click `[011]` chip → rep 011 row expands and scrolls into view, detail shows "Field Notes (1)" subsection with the 2026-04-27 preview
- Click `«` toggle → panel collapses to a vertical rail; click rail → re-expands; state persists across reload
- Resize ≤ 900px → panel becomes a fixed-position rail; expand floats over the dashboard
- Existing rep table, status pills, search, sort, and blocker ticker all work unchanged
- Click `Lessons →` → `lessons.html` shows "1 lesson across 3 reps" with the `distribution-beats-craft` card
- On lessons page, click a rep chip → returns to dashboard

Stop the server.

- [ ] **Step 6: Sanitization smoke (manual, agent-side)**

This step exercises the Telegram-agent sanitization. Without committing anything, run a temp transcript through the agent's sanitizer (the existing `sanitizeNextStep` logic). The sanitizer must strip a fake email (`john@example.com`) and a fake person name (`John Smith`).

If the agent is not yet wired up to handle field-note transcripts (planned but external to this repo), defer this check to the integration phase and note in the PR description: "deferred — covered in the rep-update agent rollout."

- [ ] **Step 7: Same-day append smoke**

```bash
mkdir -p /tmp/journal-smoke/field-notes /tmp/journal-smoke/lessons /tmp/journal-smoke/docs
cat > /tmp/journal-smoke/field-notes/2026-04-27.md <<'EOF'
---
date: 2026-04-27
reps: [11]
tags: [distribution]
---
Morning thought.
EOF
python3 -c "
import sys; sys.path.insert(0, 'scripts')
import build_journal
build_journal.build(repo_root='/tmp/journal-smoke')
import json
print(json.load(open('/tmp/journal-smoke/docs/field-notes.json'))['entries'][0]['html'])
"

cat >> /tmp/journal-smoke/field-notes/2026-04-27.md <<'EOF'

---

## 2026-04-27 19:42

Evening reflection.
EOF
python3 -c "
import sys; sys.path.insert(0, 'scripts')
import build_journal
build_journal.build(repo_root='/tmp/journal-smoke')
import json
e = json.load(open('/tmp/journal-smoke/docs/field-notes.json'))['entries'][0]
print(e['html'])
"
rm -rf /tmp/journal-smoke
```

Expected: rebuilt HTML contains both "Morning thought." and "Evening reflection." paragraphs.

- [ ] **Step 8: Phase A gate**

If any of Steps 1-7 failed, stop and fix before pushing. Once all green, proceed to Task 16.

---

## Task 16: Staged push + live verification (Phase B from the spec)

**Files:** none modified — push and verify.

- [ ] **Step 1: Push**

```bash
git push origin main
```

Expected: push succeeds.

- [ ] **Step 2: Watch GH Actions**

```bash
gh run watch
```

Confirm:
- `Build journal JSON` workflow runs and succeeds
- Existing `sync-reps-yaml.yml` is unaffected
- If the workflow made an additional commit, pull it: `git pull`

- [ ] **Step 3: Verify live**

Open `https://100repsproject.com`. Confirm parity with local:
- Left panel renders with the 2026-04-27 entry
- Rep chips clickable
- Existing rep table unaffected
- `https://100repsproject.com/lessons.html` renders the lesson

If anything is broken on live, **revert immediately**:
```bash
git revert HEAD
git push
```

- [ ] **Step 4: Done**

If the GH Action committed regenerated JSONs, that's the final state.

---

## Self-review notes

Coverage check vs the spec:
- Schema spec → Task 1
- Build script (frontmatter / rendering / sanitization / preview / walker / JSON / CLI) → Tasks 2-5
- Smoke content → Task 6
- GH Action → Task 7
- Dashboard CSS → Task 8
- Dashboard JS feed render → Task 9
- Collapse + responsive → Task 10
- Lessons page → Task 11
- Per-rep cross-link → Task 12
- rep-update skill extension → Task 13
- CLAUDE.md update → Task 14
- Local-first verification → Task 15
- Staged push → Task 16

Type/name consistency:
- Python: `parse_frontmatter`, `render_body`, `make_preview`, `build`, `_load_field_note`, `_load_lesson` — used consistently in tasks 3-5.
- JS: `fetchFieldNotes`, `renderJournal`, `wireJournalChrome`, `fieldNotesForRep` — defined and called consistently in tasks 9-12. `scrollToRep` is from existing code (line 757).
- CSS classes: `wl-rep`, `wl-lesson`, `rep-chip`, `tag-chip`, `journal-*` — emitted by `_rewrite_wikilinks` in Task 4 and the JS feed renderer in Task 9, styled by Task 8.
- Bleach allowlist (Task 4) explicitly permits `class`, `data-rep-id`, `href` on `<a>` so wikilink anchors survive sanitization.

Security:
- All HTML in JSON is bleach-sanitized server-side (Task 4). Tags allowlist excludes `<script>`, `<iframe>`, `<style>`, `<svg>`, etc. Attribute allowlist excludes all `on*` event handlers. Protocol allowlist excludes `javascript:`, `data:`, `vbscript:`. The dashboard JS therefore can safely set `innerHTML` to the `.html` field of a journal entry/lesson.
- Plain-text fields (date, preview, tags, rep ids) are inserted via `textContent` or `esc()`-escaped string interpolation.
