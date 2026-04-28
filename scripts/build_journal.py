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


_SCRIPT_TAG = re.compile(r'<script\b[^>]*>.*?</script>', re.IGNORECASE | re.DOTALL)


def render_body(body: str) -> str:
    """Render markdown to HTML, then sanitize through a strict allowlist.

    The sanitization pass ensures the resulting HTML contains only
    allowlisted tags and attributes. The dashboard JS can safely insert
    this HTML via innerHTML — no script tags, no inline event handlers,
    no dangerous href schemes survive this pipeline.
    """
    pre = _rewrite_wikilinks(body)
    raw_html = _markdown.markdown(pre, extensions=['fenced_code'])
    # Remove <script> blocks (including their content) before bleach,
    # because bleach strip=True keeps inner text by default.
    raw_html = _SCRIPT_TAG.sub('', raw_html)
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
