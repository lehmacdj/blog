import runpy
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path

SYNC_PHOTOS = Path(__file__).parent / "sync-photos"


class SyncPhotosTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.g = runpy.run_path(str(SYNC_PHOTOS))["main"].__globals__

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        root = Path(self.tmp.name)
        (root / "_notes").mkdir()
        self.saved = {
            k: self.g[k] for k in ("NOTES_DIR", "IGNORED_FILE")
        }
        self.g["NOTES_DIR"] = root / "_notes"
        self.g["IGNORED_FILE"] = root / "_ignored-photos.txt"

    def tearDown(self):
        self.g.update(self.saved)
        self.tmp.cleanup()

    def photo(self, uuid: str, caption: str):
        return self.g["Photo"](
            uuid=uuid,
            taken=datetime(2026, 1, 1, tzinfo=timezone.utc),
            original_filename="IMG_0001.HEIC",
            source=Path("/nonexistent.heic"),
            caption=caption,
        )

    def test_default_title_uses_short_first_line(self):
        self.assertEqual(
            self.g["default_title"]("Pink water\nmore detail"), "Pink water"
        )

    def test_default_title_shortens_at_word_boundary(self):
        caption = "word " * 30
        title = self.g["default_title"](caption)
        self.assertTrue(title.endswith("word…"))
        self.assertLessEqual(len(title), self.g["MAX_TITLE_LENGTH"] + 1)

    def test_note_body_keeps_caption_lines_as_paragraphs(self):
        body = self.g["note_body"]("a b.png", "one\ntwo\n\nthree")
        self.assertEqual(body, "![](</images/a b.png>)\n\none\n\ntwo\n\nthree\n")

    def test_refresh_caption_only_rewrites_body(self):
        note = self.g["NOTES_DIR"] / "abc-title.md"
        frontmatter = (
            "---\ntitle: \"Kept\"\nimage: /images/abc-x.jpeg\n"
            "photo: U1\n---\n\n"
        )
        note.write_text(frontmatter + self.g["note_body"]("abc-x.jpeg", "old"))

        photo = self.photo("U1", "new")
        self.assertTrue(self.g["refresh_caption"](photo, note))
        self.assertFalse(self.g["refresh_caption"](photo, note))
        self.assertEqual(
            note.read_text(), frontmatter + "![](/images/abc-x.jpeg)\n\nnew\n"
        )

    def test_untriaged_excludes_published_and_ignored(self):
        (self.g["NOTES_DIR"] / "abc-t.md").write_text(
            "---\ntitle: \"t\"\nphoto: PUB\n---\n\nbody\n"
        )
        self.g["write_ignored"]({"IGN"})
        photos = [self.photo(u, "c") for u in ("PUB", "IGN", "NEW")]
        remaining = [p.uuid for p in self.g["untriaged"](photos)]
        self.assertEqual(remaining, ["NEW"])

    def test_commit_message(self):
        message = self.g["commit_message"]
        self.assertEqual(message(["Pink"], 0, 0), "Publish photo Pink")
        self.assertEqual(
            message(["A", "B"], 2, 1),
            "Publish 2 photos, refresh 1 photo caption(s), ignore 2 "
            "photo(s)\n\n- A\n- B",
        )
        self.assertEqual(message([], 3, 0), "Ignore 3 photo(s)")


if __name__ == "__main__":
    unittest.main()
