import contextlib
import io
import runpy
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path
from unittest.mock import patch

import blog_utils
import image_captions as captions
from photos import Photo


class ImageCaptionTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        (self.root / "images").mkdir()
        self.source = self.root / "images/IMG_6908.jpeg"
        self.source.touch()
        self.photo = Photo(
            "PHOTO-UUID", datetime(2026, 9, 3, 5, 44, 42, tzinfo=timezone.utc),
            "IMG_6908.HEIC", Path("/library/image.heic"), "Photos caption",
        )
        self.sync = captions.CaptionSync([self.photo])
        self.metadata = {
            "DateTimeOriginal": "2026:09:03 05:44:42",
            "ImageDescription": "Stale exported caption",
        }
        wiki_patch = patch.object(captions, "WIKI_DIR", self.root)
        wiki_patch.start()
        self.addCleanup(wiki_patch.stop)
        metadata_patch = patch.object(
            captions, "image_metadata", return_value=self.metadata,
        )
        metadata_patch.start()
        self.addCleanup(metadata_patch.stop)
        self.output = contextlib.redirect_stdout(io.StringIO())
        self.output.__enter__()
        self.addCleanup(self.output.__exit__, None, None, None)

    def test_new_image_defaults_to_live_caption_and_persists_link(self):
        result = self.sync.sync("![](<images/IMG_6908.jpeg>)", "note1234")
        self.assertEqual(
            result,
            "![Photos caption](images/IMG_6908.jpeg) "
            "<!-- photo-alt: PHOTO-UUID -->",
        )
        self.assertEqual(self.sync.sync(result, "note1234"), result)
        self.photo.caption = "Changed in Photos"
        updated = self.sync.sync(result, "note1234")
        self.assertEqual(captions.images(updated)[0].alt, "Changed in Photos")

    def test_shared_marker_overwrites_even_manually_changed_alt(self):
        content = "![Edited locally](images/x.jpeg) <!-- photo-alt: PHOTO-UUID -->"
        result = self.sync.sync(content, "note1234")
        self.assertEqual(captions.images(result)[0].alt, self.photo.caption)

    def test_cleared_caption_clears_shared_alt(self):
        self.photo.caption = ""
        content = "![Old](images/x.jpeg) <!-- photo-alt: PHOTO-UUID -->"
        result = self.sync.sync(content, "note1234")
        self.assertEqual(captions.images(result)[0].alt, "")

    def test_manual_choice_is_remembered_and_later_edits_survive(self):
        content = "![Authored](images/IMG_6908.jpeg)"
        with patch("builtins.input", return_value="m") as ask:
            result = self.sync.sync(content, "note1234")
        ask.assert_called_once()
        self.assertTrue(captions.images(result)[0].manual)
        self.photo.caption = "Changed"
        result = result.replace("Authored", "Another manual edit")
        with patch("builtins.input", side_effect=AssertionError("prompt repeated")):
            self.assertEqual(self.sync.sync(result, "note1234"), result)

    def test_unify_using_alt_writes_photos_only_after_choice(self):
        content = "![Authored](images/IMG_6908.jpeg)"
        with (
            patch("builtins.input", return_value="a"),
            patch.object(captions, "set_caption") as save,
        ):
            result = self.sync.sync(content, "note1234")
        save.assert_called_once_with(self.photo, "Authored")
        self.assertEqual(self.photo.caption, "Authored")
        self.assertFalse(captions.images(result)[0].manual)

    def test_failed_photos_write_does_not_claim_unification(self):
        with patch("builtins.input", return_value="a"), patch.object(
            captions, "set_caption", side_effect=OSError("Photos denied access"),
        ):
            with self.assertRaises(OSError):
                self.sync.sync("![Authored](images/IMG_6908.jpeg)", "note1234")
        self.assertEqual(self.photo.caption, "Photos caption")

    def test_unify_using_caption_does_not_write_photos(self):
        with (
            patch("builtins.input", return_value="c"),
            patch.object(captions, "set_caption") as save,
        ):
            result = self.sync.sync("![Authored](images/IMG_6908.jpeg)", "note1234")
        save.assert_not_called()
        self.assertEqual(captions.images(result)[0].alt, "Photos caption")

    def test_edit_manual_can_intentionally_leave_alt_empty(self):
        with patch("builtins.input", side_effect=["e", ""]):
            result = self.sync.sync("![Authored](images/IMG_6908.jpeg)", "note1234")
        self.assertEqual(captions.images(result)[0].alt, "")
        self.assertTrue(captions.images(result)[0].manual)
        self.assertEqual(self.sync.sync(result, "note1234"), result)

    def test_noninteractive_conflict_requires_a_choice(self):
        with patch("builtins.input", side_effect=EOFError):
            with self.assertRaises(captions.CaptionChoiceRequired):
                self.sync.sync("![Authored](images/IMG_6908.jpeg)", "note1234")

    def test_existing_unmarked_images_only_prompt_during_review(self):
        content = "![Authored](images/IMG_6908.jpeg)"
        previous = "![Authored](/images/note1234-IMG_6908.jpeg)"
        with patch("builtins.input", side_effect=AssertionError("unexpected prompt")):
            self.assertEqual(self.sync.sync(content, "note1234", previous), content)
        with patch("builtins.input", return_value="c"):
            result = self.sync.sync(content, "note1234", previous, review=True)
        self.assertEqual(captions.images(result)[0].uuid, "PHOTO-UUID")

    def test_review_can_make_equal_shared_text_manual(self):
        content = "![Photos caption](images/x.jpeg) <!-- photo-alt: PHOTO-UUID -->"
        with patch("builtins.input", return_value="m"):
            result = self.sync.sync(content, "note1234", review=True)
        self.assertTrue(captions.images(result)[0].manual)

    def test_new_use_of_an_already_published_image_gets_default(self):
        content = (
            "![Photos caption](images/IMG_6908.jpeg) "
            "<!-- photo-alt: PHOTO-UUID -->\n"
            "![](images/IMG_6908.jpeg)"
        )
        previous = "![Photos caption](/images/note1234-IMG_6908.jpeg)"
        result = self.sync.sync(content, "note1234", previous)
        self.assertEqual(captions.images(result)[1].alt, "Photos caption")

    def test_missing_photo_preserves_shared_alt_and_link(self):
        content = "![Old](images/x.jpeg) <!-- photo-alt: MISSING -->"
        self.assertEqual(self.sync.sync(content, "note1234"), content)

    def test_matching_requires_unique_name_and_time(self):
        self.assertIs(
            captions.match_photo(self.source, self.metadata, [self.photo]),
            self.photo,
        )
        self.assertIsNone(captions.match_photo(
            self.source, self.metadata, [self.photo, self.photo],
        ))
        self.assertIsNone(captions.match_photo(self.source, {}, [self.photo]))
        self.assertIsNone(captions.match_photo(
            Path("different.jpeg"), self.metadata, [self.photo],
        ))

    def test_unmatched_export_defaults_without_inventing_uuid(self):
        result = captions.CaptionSync([]).sync("![](images/IMG_6908.jpeg)", "note1234")
        image = captions.images(result)[0]
        self.assertEqual(image.alt, "Stale exported caption")
        self.assertEqual(image.uuid, "")

    def test_markdown_and_html_escape_caption_and_keep_attributes(self):
        self.photo.caption = 'A [brownie] & <plate> "here" \\ *bold* `code`\nnext'
        for markup in (
            "![](images/IMG_6908.jpeg)",
            "![[images/IMG_6908.jpeg]]",
            '<img class="photo" src="images/IMG_6908.jpeg" loading="lazy">',
            "<img src='images/IMG_6908.jpeg' alt='' />",
        ):
            with self.subTest(markup=markup):
                result = self.sync.sync(markup, "note1234")
                self.assertEqual(
                    captions.images(result)[0].alt,
                    captions.plain_text(self.photo.caption),
                )
                self.assertEqual(self.sync.sync(result, "note1234"), result)
                if 'class="photo"' in markup:
                    self.assertIn('class="photo"', result)
                    self.assertIn('loading="lazy"', result)

    def test_code_comments_and_remote_images_are_untouched(self):
        content = (
            "```md\n![](images/IMG_6908.jpeg)\n```\n"
            "`![](images/IMG_6908.jpeg)`\n"
            "<!-- ![](images/IMG_6908.jpeg) -->\n"
            "![](https://example.com/photo.jpeg)"
        )
        self.assertEqual(self.sync.sync(content, "note1234"), content)

    def test_sync_note_persists_marker_in_wiki_and_blog(self):
        note_id = "note1234"
        wiki = self.root / f"{note_id}.md"
        blog_dir = self.root / "blog"
        blog_dir.mkdir()
        blog = blog_dir / f"{note_id}-title.md"
        wiki.write_text('---\ntitle: Title\ntags: []\n---\n\n![](images/IMG_6908.jpeg)\n')
        blog.write_text('---\ntitle: Title\ndate: today\n---\n\nBefore\n')
        module = runpy.run_path("bin/sync-notes")["sync_note"].__globals__
        with patch.dict(module, {
            "WIKI_DIR": self.root, "NOTES_DIR": blog_dir,
            "find_blog_note": lambda _: blog,
            "ensure_published_link": lambda *_: False,
        }), patch.object(blog_utils, "_copy_wiki_image", return_value=(
            self.root / "note1234-IMG_6908.jpeg", False,
        )):
            module["sync_note"](note_id, captions=self.sync)
            self.assertIn("<!-- photo-alt: PHOTO-UUID -->", wiki.read_text())
            self.assertIn(
                "![Photos caption](/images/note1234-IMG_6908.jpeg)",
                blog.read_text(),
            )
            self.assertIsNone(module["sync_note"](note_id, captions=self.sync))
            self.photo.caption = "Changed"
            module["sync_note"](note_id, captions=self.sync)
            self.assertIn("![Changed]", wiki.read_text())
            self.assertIn("![Changed]", blog.read_text())

    def test_copy_images_preserves_escaped_alt_and_markers(self):
        self.photo.caption = "A [brownie] & *crumbs*"
        content = self.sync.sync("![](images/IMG_6908.jpeg)", "note1234")
        with patch.object(blog_utils, "_copy_wiki_image", return_value=(
            Path("note1234-IMG_6908.jpeg"), True,
        )):
            result, copied, _ = blog_utils.copy_images(content, "note1234")
        image = captions.images(result)[0]
        self.assertEqual(image.path, "/images/note1234-IMG_6908.jpeg")
        self.assertEqual(image.alt, self.photo.caption)
        self.assertEqual(image.uuid, self.photo.uuid)
        self.assertEqual(len(copied), 1)

    def test_copy_images_ignores_code_and_preserves_html_other_attributes(self):
        content = (
            '`![](images/code.jpeg)`\n'
            '<img data-src="lazy.jpeg" src="images/a%20b.jpeg" '
            'alt="Text &amp; more" loading="lazy"> '
            '<!-- photo-alt: PHOTO-UUID manual -->'
        )
        with patch.object(blog_utils, "_copy_wiki_image", return_value=(
            Path("note1234-a b.jpeg"), True,
        )) as copy:
            result, _, _ = blog_utils.copy_images(content, "note1234")
        copy.assert_called_once_with("images/a%20b.jpeg", "note1234", "PHOTO-UUID")
        self.assertIn('data-src="lazy.jpeg"', result)
        self.assertIn('src="/images/note1234-a%20b.jpeg"', result)
        self.assertIn('alt="Text &amp; more" loading="lazy"', result)
        self.assertIn('<!-- photo-alt: PHOTO-UUID manual -->', result)


if __name__ == "__main__":
    unittest.main()
