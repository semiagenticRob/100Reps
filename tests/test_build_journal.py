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
        raw = "---\ndate: 2026-04-26\nreps: []\ntags: []\n---\nBody\n"
        meta, _ = build_journal.parse_frontmatter(raw)
        self.assertIsInstance(meta['date'], str)
        self.assertEqual(meta['date'], '2026-04-26')


if __name__ == '__main__':
    unittest.main()
