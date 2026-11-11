import struct
import tempfile
import unittest
import zlib
from pathlib import Path
from unittest.mock import patch

import blog_utils as blog


def png(width: int, height: int) -> bytes:
    """A small, dependency-free grayscale PNG fixture."""
    def chunk(name, data):
        return (struct.pack(">I", len(data)) + name + data
                + struct.pack(">I", zlib.crc32(name + data)))
    header = struct.pack(">2I5B", width, height, 8, 0, 0, 0, 0)
    rows = b"".join(b"\0" + bytes([y % 256]) * width for y in range(height))
    return (b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", header)
            + chunk(b"IDAT", zlib.compress(rows)) + chunk(b"IEND", b""))


class ImageExportTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)

    def source(self, name, width, height):
        path = self.root / name
        path.write_bytes(png(width, height))
        return path

    def test_export_bounds_size_without_upscaling_or_changing_source(self):
        for width, height in ((2400, 1200), (24, 12)):
            source = self.source(f"{width}.png", width, height)
            before = source.read_bytes()
            dest = self.root / f"export-{width}.png"
            blog.import_image(source, dest)
            self.assertEqual(blog.image_size(dest),
                             (2048, 1024) if width > 2048 else (width, height))
            self.assertEqual(source.read_bytes(), before)

    def test_identical_exports_share_and_different_crops_remain_separate(self):
        source = self.source("original.png", 24, 12)
        copy = self.source("renamed.png", 24, 12)
        crop = self.source("cropped.png", 12, 12)
        output = self.root / "blog"
        with patch("photos.load_photos", side_effect=AssertionError("DB read")):
            first, added = blog.export_photo_image(source, "UUID", directory=output)
            second, reused = blog.export_photo_image(copy, "UUID", directory=output)
            variant, _ = blog.export_photo_image(crop, "UUID", directory=output)
        self.assertTrue(added)
        self.assertFalse(reused)
        self.assertEqual(first, second)
        self.assertNotEqual(first, variant)
        self.assertTrue(first.name.startswith("UUID-"))
        self.assertEqual(len(list(output.iterdir())), 2)

    def test_failed_export_keeps_previous_good_file(self):
        source = self.source("source.png", 24, 12)
        dest = self.root / "published.png"
        dest.write_bytes(b"previous")
        with patch.object(blog, "_render_image", side_effect=ValueError("bad image")):
            with self.assertRaisesRegex(ValueError, "bad image"):
                blog.import_image(source, dest)
        self.assertEqual(dest.read_bytes(), b"previous")

    def test_cover_and_body_use_the_same_exported_path(self):
        body = "![](images/photo.jpeg) <!-- photo-alt: UUID manual -->"
        exported = self.root / "UUID-fingerprint.jpeg"
        with patch.object(blog, "_copy_wiki_image", return_value=(exported, True)) as copy:
            body, copied, cover = blog.copy_images(
                body, "note1234", frontmatter_image="images/photo.jpeg",
            )
        copy.assert_called_once_with("images/photo.jpeg", "note1234", "UUID")
        self.assertIn(f"]({cover})", body)
        frontmatter = blog.build_frontmatter(
            "note1234", "Title", "today", [], {}, image_path=cover,
        )
        self.assertEqual(blog.parse_frontmatter(frontmatter)[0]["image"], cover)
        self.assertEqual(copied, [exported])


if __name__ == "__main__":
    unittest.main()
