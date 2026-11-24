import contextlib
import io
import os
import runpy
import subprocess
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path
from unittest.mock import Mock, patch

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

    def test_caption_summary_uses_short_first_line(self):
        self.assertEqual(
            self.g["caption_summary"]("Pink water\nmore detail"), "Pink water"
        )

    def test_caption_summary_shortens_at_word_boundary(self):
        caption = "word " * 30
        title = self.g["caption_summary"](caption)
        self.assertTrue(title.endswith("word…"))
        self.assertLessEqual(len(title), self.g["MAX_TITLE_LENGTH"] + 1)

    def test_note_body_keeps_caption_lines_as_paragraphs(self):
        body = self.g["note_body"]("a b.png", "one\ntwo\n\nthree")
        self.assertEqual(
            body, "![one two three](</images/a b.png>)\n\none\n\ntwo\n\nthree\n",
        )

    def test_refresh_note_updates_date_and_body_only(self):
        note = self.g["NOTES_DIR"] / "abc-title.md"
        frontmatter = (
            "---\ntitle: \"Kept\"\ndate: {}\nimage: /images/abc-x.jpeg\n"
            "photo: U1\n---\n\n"
        )
        note.write_text(
            frontmatter.format("2026-11-03 02:27 -0500")
            + self.g["note_body"]("abc-x.jpeg", "old", uuid="U1")
        )

        photo = self.photo("U1", "new")
        self.assertTrue(self.g["refresh_note"](photo, note))
        self.assertFalse(self.g["refresh_note"](photo, note))
        self.assertEqual(
            note.read_text(),
            frontmatter.format("2026-01-01 00:00 +0000")
            + "![new](/images/abc-x.jpeg) <!-- photo-alt: U1 -->\n\nnew\n",
        )

    def test_post_date_uses_photo_time_zone(self):
        photo = self.photo("U1", "c")
        photo.taken = datetime(
            2026, 10, 26, 22, 46, tzinfo=timezone(timedelta(hours=-4)),
        )
        self.assertEqual(self.g["post_date"](photo), "2026-10-26 22:46 -0400")

    def test_untitled_frontmatter(self):
        fm = self.g["photo_frontmatter"](
            "abc", None, "Pink water\nmore", "2026-01-01 00:00 +0000",
            "abc-x.jpeg", "U1",
        )
        metadata, _ = self.g["parse_frontmatter"](fm + "\n")
        self.assertEqual(metadata["title"], "Pink water")
        self.assertEqual(metadata["untitled"], "true")
        self.assertEqual(metadata["permalink"], "/abc")
        self.assertNotIn("redirect_from", fm)
        self.assertEqual(self.g["photo_note_name"]("abc", None), "abc.md")

    def test_titled_frontmatter(self):
        fm = self.g["photo_frontmatter"](
            "abc", "My Title", "caption", "2026-01-01 00:00 +0000",
            "abc-x.jpeg", "U1",
        )
        metadata, _ = self.g["parse_frontmatter"](fm + "\n")
        self.assertEqual(metadata["title"], "My Title")
        self.assertNotIn("untitled", metadata)
        self.assertEqual(metadata["permalink"], "/abc/my-title")
        self.assertEqual(
            self.g["photo_note_name"]("abc", "My Title"), "abc-my-title.md"
        )

    def test_parse_tag_input(self):
        self.assertEqual(
            self.g["parse_tag_input"]("Mahjong, riichi  photo,mahjong Go Pro"),
            ["mahjong", "riichi", "go", "pro"],
        )
        self.assertEqual(self.g["parse_tag_input"](""), [])

    def test_frontmatter_tags_start_with_photo(self):
        fm = self.g["photo_frontmatter"](
            "abc", None, "c", "d", "abc-x.jpeg", "U1", ["mahjong"],
        )
        self.assertIn("tags: [photo, mahjong]\n", fm)

    def test_refresh_note_updates_untitled_summary(self):
        note = self.g["NOTES_DIR"] / "abc.md"
        note.write_text(
            self.g["photo_frontmatter"](
                "abc", None, "old", "d", "abc-x.jpeg", "U1",
            ) + "\n\n" + self.g["note_body"]("abc-x.jpeg", "old", uuid="U1")
        )
        self.assertTrue(
            self.g["refresh_note"](self.photo("U1", "new words"), note)
        )
        metadata, body = self.g["parse_frontmatter"](note.read_text())
        self.assertEqual(metadata["title"], "new words")
        self.assertEqual(metadata["untitled"], "true")
        self.assertEqual(
            body, "![new words](/images/abc-x.jpeg) "
            "<!-- photo-alt: U1 -->\n\nnew words\n",
        )

    def test_untriaged_excludes_published_and_ignored(self):
        (self.g["NOTES_DIR"] / "abc-t.md").write_text(
            "---\ntitle: \"t\"\nphoto: PUB\n---\n\nbody\n"
        )
        self.g["write_ignored"]({"IGN"})
        photos = [self.photo(u, "c") for u in ("PUB", "IGN", "NEW")]
        remaining = [p.uuid for p in self.g["untriaged"](photos)]
        self.assertEqual(remaining, ["NEW"])

    def test_refresh_preserves_manual_alt_including_empty(self):
        for alt in ("Manual description", ""):
            with self.subTest(alt=alt):
                note = self.g["NOTES_DIR"] / "abc.md"
                note.write_text(
                    self.g["photo_frontmatter"](
                        "abc", None, "old", "d", "abc-x.jpeg", "U1",
                    ) + "\n\n" + self.g["note_body"](
                        "abc-x.jpeg", "old", uuid="U1", alt=alt,
                    )
                )
                self.g["refresh_note"](self.photo("U1", "new"), note)
                body = self.g["parse_frontmatter"](note.read_text())[1]
                image = self.g["images"](body)[0]
                self.assertEqual(image.alt, alt)
                self.assertTrue(image.manual)
                self.assertTrue(body.endswith("\n\nnew\n"))

    def test_refresh_migrates_legacy_empty_alt_to_shared(self):
        note = self.g["NOTES_DIR"] / "abc.md"
        note.write_text(
            self.g["photo_frontmatter"](
                "abc", None, "old", "d", "abc-x.jpeg", "U1",
            ) + "\n\n![](/images/abc-x.jpeg)\n\nold\n"
        )
        self.g["refresh_note"](self.photo("U1", "new"), note)
        self.assertIn("![new]", note.read_text())
        self.assertIn("<!-- photo-alt: U1 -->", note.read_text())

    def test_linked_note_sync_updates_images_without_publishing_other_edits(self):
        root = Path(self.tmp.name)
        wiki = root / "wiki"
        wiki.mkdir()
        source = wiki / "note1234.md"
        source.write_text(
            "Draft prose that must stay private\n"
            "![Old](images/x.jpeg) <!-- photo-alt: U1 -->\n"
            "![Manual edit](images/y.jpeg) <!-- photo-alt: U2 manual -->\n"
        )
        blog = self.g["NOTES_DIR"] / "note1234-title.md"
        blog.write_text(
            "---\ntitle: Title\n---\n\nPublished prose\n"
            "![Old](/images/note1234-x.jpeg) <!-- photo-alt: U1 -->\n"
            "![Old manual](/images/note1234-y.jpeg) "
            "<!-- photo-alt: U2 manual -->\n"
        )
        photos = [self.photo("U1", "New caption"), self.photo("U2", "Other")]
        with patch.dict(self.g, {"WIKI_DIR": wiki}):
            self.assertEqual(self.g["refresh_linked_notes"](photos), 1)
            self.assertEqual(self.g["refresh_linked_notes"](photos), 0)
        self.assertIn("![New caption]", source.read_text())
        self.assertIn("![New caption]", blog.read_text())
        self.assertIn("![Manual edit]", blog.read_text())
        self.assertIn("Published prose", blog.read_text())
        self.assertNotIn("Draft prose", blog.read_text())
        self.assertEqual(self.g["untriaged"](photos), [])

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

    def test_edit_tags_adds_and_removes(self):
        edit = self.g["edit_tags"]
        self.assertEqual(
            edit(["balloons", "travel"], "-travel Sunset, balloons"),
            ["balloons", "sunset"],
        )
        self.assertEqual(edit(["a"], "-a"), [])
        self.assertEqual(edit([], "photo, Go"), ["go"])

    def test_describe_tags_flags_new(self):
        describe = self.g["describe_tags"]
        self.assertEqual(
            describe(["mahjong", "balloons"], {"mahjong"}),
            "mahjong, balloons (new)",
        )
        self.assertEqual(describe([], set()), "none")

    def test_triage_advances_to_alt_and_can_go_back_to_edit_tags(self):
        photo = self.photo("U1", "A caption")
        photo.keywords = ["Old"]
        publish = Mock(return_value="/abc/my-title")
        output = io.StringIO()
        with (
            patch.dict(self.g, {
                "collect_all_tags": lambda: {"photo", "old"},
                "preview": lambda photo: None,
                "publish_photo": publish,
            }),
            patch("builtins.input", side_effect=[
                "t", "A title", "sunset", "-", "-old travel", "A description",
            ]) as read_input,
            contextlib.redirect_stdout(output),
        ):
            self.assertEqual(self.g["triage"]([photo]), (["A title"], 0))
        prompts = [call.args[0].strip() for call in read_input.call_args_list]
        self.assertEqual(len(prompts), 6)
        self.assertTrue(prompts[3].startswith("Alt text"))
        self.assertTrue(prompts[4].startswith("Add tags"))
        self.assertIn("Tags: old, sunset (new)", output.getvalue())
        publish.assert_called_once_with(
            photo, "A title", ["sunset", "travel"], alt="A description",
        )

    def test_sync_keywords_sets_post_tags(self):
        (self.g["NOTES_DIR"] / "a.md").write_text(
            "---\ntags: [photo, mahjong, riichi]\nphoto: U1\n---\n\nb\n"
        )
        (self.g["NOTES_DIR"] / "b.md").write_text(
            "---\ntags: [photo, same]\nphoto: U2\n---\n\nb\n"
        )
        (self.g["NOTES_DIR"] / "c.md").write_text(
            "---\ntags: [photo]\nphoto: U3\n---\n\nb\n"
        )
        photos = [self.photo(u, "c") for u in ("U1", "U2", "U3")]
        photos[0].keywords = ["Balloons", "mahjong"]
        photos[1].keywords = ["same"]
        photos[2].keywords = ["photo"]
        saved = []
        with patch.dict(self.g, {
            "set_keywords": lambda photo, tags: saved.append((photo.uuid, tags)),
        }), contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(self.g["sync_keywords"](photos), 2)
            self.assertEqual(self.g["sync_keywords"](photos), 0)
        self.assertEqual(saved, [("U1", ["mahjong", "riichi"]), ("U3", [])])

    def test_sync_keywords_continues_after_failure(self):
        (self.g["NOTES_DIR"] / "a.md").write_text(
            "---\ntags: [photo, x]\nphoto: U1\n---\n\nb\n"
        )
        photo = self.photo("U1", "c")

        def fail(photo, tags):
            raise subprocess.CalledProcessError(1, ["osascript"])

        with patch.dict(self.g, {"set_keywords": fail}), \
                contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(self.g["sync_keywords"]([photo]), 0)
        self.assertEqual(photo.keywords, [])

    def test_commit_message(self):
        message = self.g["commit_message"]
        self.assertEqual(message(["Pink"], 0), "Publish photo Pink")
        self.assertEqual(
            message(["A", "B"], 1),
            "Publish 2 photos, update 1 photo post(s) from Photos"
            "\n\n- A\n- B",
        )
        self.assertEqual(
            message([], 3), "Update 3 photo post(s) from Photos"
        )


if __name__ == "__main__":
    unittest.main()
