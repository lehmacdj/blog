import contextlib
import io
import os
import runpy
import subprocess
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

    def edit_with(self, new_text: str, fail_save: bool = False):
        """Run edit_caption with an editor that writes new_text and a fake
        Photos write. Returns (photo, captions saved to Photos)."""
        root = Path(self.tmp.name)
        (root / "new.txt").write_text(new_text)
        editor = root / "editor"
        editor.write_text(f'#!/bin/sh\ncp "{root / "new.txt"}" "$1"\n')
        editor.chmod(0o755)
        saved = []

        def fake_set_caption(photo, caption):
            if fail_save:
                raise subprocess.CalledProcessError(
                    1, ["osascript"], stderr=b"not allowed"
                )
            saved.append(caption)

        photo = self.photo("U1", "old caption")
        old = (self.g["set_caption"], os.environ.get("VISUAL"))
        self.g["set_caption"] = fake_set_caption
        os.environ["VISUAL"] = str(editor)
        try:
            with contextlib.redirect_stdout(io.StringIO()):
                self.g["edit_caption"](photo)
        finally:
            self.g["set_caption"] = old[0]
            if old[1] is None:
                del os.environ["VISUAL"]
            else:
                os.environ["VISUAL"] = old[1]
        return photo, saved

    def test_edit_caption_saves_to_photos(self):
        photo, saved = self.edit_with("new caption\nline two\n")
        self.assertEqual(saved, ["new caption\nline two"])
        self.assertEqual(photo.caption, "new caption\nline two")

    def test_edit_caption_rejects_empty(self):
        photo, saved = self.edit_with("  \n")
        self.assertEqual(saved, [])
        self.assertEqual(photo.caption, "old caption")

    def test_edit_caption_keeps_old_caption_if_save_fails(self):
        photo, saved = self.edit_with("new", fail_save=True)
        self.assertEqual(photo.caption, "old caption")

    def test_commit_message(self):
        message = self.g["commit_message"]
        self.assertEqual(message(["Pink"], 0), "Publish photo Pink")
        self.assertEqual(
            message(["A", "B"], 1),
            "Publish 2 photos, refresh 1 photo caption(s)\n\n- A\n- B",
        )
        self.assertEqual(message([], 3), "Refresh 3 photo caption(s)")


if __name__ == "__main__":
    unittest.main()
