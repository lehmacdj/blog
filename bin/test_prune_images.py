import runpy
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


class PruneImagesTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.script = runpy.run_path("bin/prune-images")

    def test_preserves_sources_and_drafts_but_ignores_stale_caches(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            assets = root / "images"
            assets.mkdir()
            for name in ("cover.png", "a b.png", "x&y.svg", "draft.jpeg",
                         "old.jpeg", "video.mov"):
                (assets / name).write_bytes(b"\xff")
            (root / "note.md").write_text(
                '---\nimage: /images/cover.png\n---\n'
                '![alt](/images/a%20b.png)\n'
                '<img src="/images/x&amp;y.svg">\n'
            )
            (root / "_drafts").mkdir()
            (root / "_drafts/draft.md").write_text('![](images/draft.jpeg)')
            for folder in ("_site", ".jekyll-cache"):
                (root / folder).mkdir()
                (root / folder / "stale.html").write_text(
                    '<img src="/images/old.jpeg">',
                )
            unused = self.script["unused_images"](root)
            self.assertEqual(unused, [assets / "old.jpeg"])
            with patch.dict(self.script["main"].__globals__, {"BLOG_DIR": root}):
                with patch("sys.argv", ["prune-images"]):
                    self.script["main"]()
                self.assertTrue((assets / "old.jpeg").exists())
                with patch("sys.argv", ["prune-images", "--apply"]):
                    self.script["main"]()
            self.assertEqual(self.script["unused_images"](root), [])
            self.assertTrue((assets / "video.mov").exists())

    def test_keeps_referenced_variants_css_assets_and_symlinks(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            assets = root / "images"
            assets.mkdir()
            for name in ("UUID-crop.png", "UUID-old.png", "css image.png"):
                (assets / name).write_bytes(b"\xff")
            (assets / "linked.png").symlink_to(assets / "UUID-crop.png")
            (root / "page.html").write_text('src="/images/UUID-crop.png"')
            (root / "style.css").write_text('url("/images/css\\ image.png")')
            self.assertEqual(self.script["unused_images"](root),
                             [assets / "UUID-old.png"])


if __name__ == "__main__":
    unittest.main()
