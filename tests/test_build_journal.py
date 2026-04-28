import json
import shutil
import sys
import tempfile
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
        raw = "---\ndate: 2026-04-26\nreps: []\ntags: []\n---\nBody\n"
        meta, _ = build_journal.parse_frontmatter(raw)
        self.assertIsInstance(meta['date'], str)
        self.assertEqual(meta['date'], '2026-04-26')


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

    def test_sanitization_strips_style_tags(self):
        html = build_journal.render_body("<style>body{background:red}</style>Visible.\n")
        self.assertNotIn('<style', html)
        self.assertNotIn('background:red', html)
        self.assertIn('Visible', html)

    def test_sanitization_strips_iframe_tags(self):
        html = build_journal.render_body('<iframe src="evil"></iframe>after\n')
        self.assertNotIn('<iframe', html)
        self.assertNotIn('evil', html)


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


if __name__ == '__main__':
    unittest.main()
