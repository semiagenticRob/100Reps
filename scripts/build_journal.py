"""Build script for the 100 Reps Field Notes & Lessons journal.

Walks `field-notes/` and `lessons/` at the repo root, parses each markdown
file (frontmatter + body), renders body markdown to HTML, sanitizes the
HTML through a strict allowlist, and writes `docs/field-notes.json` and
`docs/lessons.json`.
"""
from __future__ import annotations

import datetime as _dt
import json
import re
import sys
from pathlib import Path
from typing import Any

import bleach
import markdown as _markdown
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


_RAW_TEXT_TAG = re.compile(
    r'<(script|style|noscript|template|xmp|iframe)\b[^>]*>.*?</\1>',
    re.IGNORECASE | re.DOTALL,
)


def render_body(body: str) -> str:
    """Render markdown to HTML, then sanitize through a strict allowlist.

    The sanitization pass ensures the resulting HTML contains only
    allowlisted tags and attributes. The dashboard JS can safely insert
    this HTML via innerHTML — no script tags, no inline event handlers,
    no dangerous href schemes survive this pipeline.
    """
    pre = _rewrite_wikilinks(body)
    raw_html = _markdown.markdown(pre, extensions=['fenced_code'])
    # Remove raw-text element blocks (script, style, noscript, template, xmp, iframe)
    # including their content, before bleach. Bleach with strip=True keeps inner
    # text by default for these elements.
    raw_html = _RAW_TEXT_TAG.sub('', raw_html)
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
