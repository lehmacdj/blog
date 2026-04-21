import runpy
import tempfile
import unittest
from pathlib import Path

from blog_utils import (
    build_frontmatter,
    parse_frontmatter,
    parse_yaml_scalar,
    serialize_yaml_scalar,
)


class TitleFrontmatterTests(unittest.TestCase):
    def test_lsp_scalar_round_trip(self):
        title = 'She said "hi" about C:\\tmp\nnext line\t\N{SNOWMAN}'
        scalar = serialize_yaml_scalar(title)

        self.assertEqual(parse_yaml_scalar(scalar), title)
        self.assertNotIn("\n", scalar)

    def test_parse_frontmatter_decodes_lsp_title(self):
        title = 'A "quoted" title with \\slashes'
        content = (
            "---\n"
            f"title: {serialize_yaml_scalar(title)}\n"
            "title_wls_transcluded: true\n"
            "---\n\n"
            "# Source heading\n"
        )

        metadata, body = parse_frontmatter(content)

        self.assertEqual(metadata["title"], title)
        self.assertEqual(metadata["title_wls_transcluded"], "true")
        self.assertEqual(body, "# Source heading\n")

    def test_blog_frontmatter_reencodes_title_safely(self):
        title = 'A "quoted" title with \\slashes'
        frontmatter = build_frontmatter(
            "note1234",
            title,
            "2026-07-14 12:00 -0400",
            [],
            {},
        )

        metadata, _ = parse_frontmatter(frontmatter + "\n\nBody\n")

        self.assertEqual(metadata["title"], title)
        self.assertIn(f"title: {serialize_yaml_scalar(title)}", frontmatter)

    def test_single_quoted_yaml_remains_supported(self):
        self.assertEqual(parse_yaml_scalar("'it''s fine'"), "it's fine")

    def test_frontmatter_delimiters_must_be_complete_lines(self):
        title = "A title with --- inside it"
        content = (
            "---\n"
            f"title: {serialize_yaml_scalar(title)}\n"
            "---\n\n"
            "Body\n"
        )

        metadata, body = parse_frontmatter(content)

        self.assertEqual(metadata["title"], title)
        self.assertEqual(body, "Body\n")

    def test_nested_title_is_not_treated_as_top_level(self):
        metadata, _ = parse_frontmatter(
            "---\nseo:\n  title: Nested\ndate: today\n---\n"
        )

        self.assertNotIn("title", metadata)
        self.assertEqual(metadata["date"], "today")


class PublishingTitleTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.publish_module = runpy.run_path("bin/publish-note")
        cls.sync_module = runpy.run_path("bin/sync-notes")

    def test_publish_requires_frontmatter_title(self):
        with tempfile.TemporaryDirectory() as directory:
            wiki_dir = Path(directory)
            (wiki_dir / "note1234.md").write_text(
                "---\ndate: today\n---\n\n# Legacy H1\n"
            )
            globals_ = self.publish_module["publish_note"].__globals__
            old_wiki_dir = globals_["WIKI_DIR"]
            globals_["WIKI_DIR"] = wiki_dir
            try:
                with self.assertRaisesRegex(ValueError, "No `title:`"):
                    self.publish_module["publish_note"]("note1234")
            finally:
                globals_["WIKI_DIR"] = old_wiki_dir

    def test_sync_warns_without_frontmatter_title(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            wiki_dir = root / "wiki"
            wiki_dir.mkdir()
            wiki_path = wiki_dir / "note1234.md"
            wiki_path.write_text("---\ndate: today\n---\n\n# Legacy H1\n")
            blog_path = root / "note1234-legacy-h1.md"
            blog_path.write_text(
                "---\ntitle: \"Legacy H1\"\ndate: today\n---\n\nBody\n"
            )
            globals_ = self.sync_module["sync_note"].__globals__
            old_wiki_dir = globals_["WIKI_DIR"]
            old_find_blog_note = globals_["find_blog_note"]
            globals_["WIKI_DIR"] = wiki_dir
            globals_["find_blog_note"] = lambda _: blog_path
            try:
                result = self.sync_module["sync_note"]("note1234")
            finally:
                globals_["WIKI_DIR"] = old_wiki_dir
                globals_["find_blog_note"] = old_find_blog_note

            self.assertEqual(
                result,
                [f"warning: no `title:` in frontmatter of {wiki_path}"],
            )


if __name__ == "__main__":
    unittest.main()
