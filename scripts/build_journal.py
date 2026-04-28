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
