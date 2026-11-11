"""Caption defaults and explicit Photos links in Markdown image comments.

    ![Alt text](images/example.jpeg) <!-- photo-alt: PHOTO-UUID -->
    ![Independent alt](images/example.jpeg) <!-- photo-alt: PHOTO-UUID manual -->

Photos is canonical for shared alt text. Manual links remember the decision
without overwriting the author's text. Unlinked exports can supply a default
caption, but cannot follow later edits in Photos.
"""

import json
import subprocess
from collections import Counter
from pathlib import Path
from urllib.parse import unquote

from blog_utils import WIKI_DIR, blog_image_name
from photos import Photo, load_photos, set_caption
from image_markup import images, plain_text


def image_metadata(path: Path) -> dict:
    result = subprocess.run(
        ["exiftool", "-json", "-Description", "-ImageDescription",
         "-Caption-Abstract", "-DateTimeOriginal", str(path)],
        check=True, capture_output=True, text=True,
    )
    return json.loads(result.stdout)[0]


def match_photo(path: Path, metadata: dict, photos: list[Photo]) -> Photo | None:
    """Export identifiers vary; require a unique filename AND capture time."""
    taken = metadata.get("DateTimeOriginal")
    if not taken:
        return None
    matches = [p for p in photos
               if Path(p.original_filename).stem.casefold() == path.stem.casefold()
               and p.taken.strftime("%Y:%m:%d %H:%M:%S") == taken]
    return matches[0] if len(matches) == 1 else None


class CaptionChoiceRequired(ValueError):
    pass


def choose_alt(label: str, alt: str, caption: str, linked: bool) -> tuple[str, bool]:
    """Return (chosen text, manual). A noninteractive conflict must not publish."""
    print(f"\nImage: {label}\n  Alt text: {alt}\n  Caption: {caption}")
    while True:
        choices = "[c]aption for both, [a]lt text for both" if linked else (
            "[c]opy exported caption"
        )
        try:
            answer = input(
                f"  {choices}, [m]anual (keep alt), [e]dit manual, [q]uit? "
            ).strip().lower()
            if answer == "c":
                return caption, False
            if answer == "a" and linked:
                return alt, False
            if answer == "m":
                return alt, True
            if answer == "e":
                return input("  Manual alt text (may be empty): ").strip(), True
            if answer == "q":
                raise CaptionChoiceRequired("Image caption choice cancelled.")
        except EOFError as e:
            raise CaptionChoiceRequired(
                f"Choose alt text for {label} in an interactive terminal."
            ) from e


class CaptionSync:
    def __init__(self, photos: list[Photo] | None = None):
        self._photos = photos

    @property
    def photos(self) -> list[Photo]:
        if self._photos is None:
            try:
                self._photos = load_photos()
            except (OSError, RuntimeError) as e:
                print(f"  Warning: {e}; Photos caption links are unavailable.")
                self._photos = []
        return self._photos

    def sync(
        self, content: str, note_id: str, previous: str = "",
        *, review: bool = False, linked_only: bool = False,
    ) -> str:
        """Update image text and markers, leaving unrelated prose untouched.

        previous is the published body: existing unmarked images are left
        alone unless explicitly reviewed. Marked images always synchronize.
        """
        existing = Counter(unquote(image.path) for image in images(previous))
        replacements = []
        for image in images(content):
            source = WIKI_DIR / unquote(image.path)
            published_path = "/images/" + blog_image_name(note_id, source)
            already_published = existing[published_path] > 0
            if already_published:
                existing[published_path] -= 1
            photo = None
            caption = ""
            if image.uuid:
                if image.manual and not review:
                    continue
                photo = next((p for p in self.photos if p.uuid == image.uuid), None)
                if photo is None:
                    print(f"  Warning: Photos asset {image.uuid} is unavailable; "
                          f"leaving alt text for {image.path} unchanged.")
                    continue
                caption = photo.caption
            else:
                if linked_only or image.path.startswith(("/", "http:", "https:")):
                    continue
                if already_published and not review:
                    continue
                if not source.is_file():
                    continue
                metadata = image_metadata(source)
                photo = match_photo(source, metadata, self.photos)
                caption = photo.caption if photo else next(
                    (metadata[k] for k in
                     ("Description", "ImageDescription", "Caption-Abstract")
                     if metadata.get(k)), "",
                )
                if not caption and not photo:
                    continue

            manual = False
            alt = caption
            # Explicit shared markers make Photos canonical. Review lets the
            # author opt out, even when the current texts happen to agree.
            if review or (not image.uuid and image.alt
                          and plain_text(image.alt) != plain_text(caption)):
                alt, manual = choose_alt(image.path, image.alt, caption, bool(photo))
                if photo and not manual and alt != caption:
                    set_caption(photo, alt)
                    photo.caption = alt
            if not photo and not manual:
                print(f"  {image.path}: using exported caption; no unique Photos "
                      "match, so future Photos edits will not synchronize.")
            replacement = image.render(alt, photo.uuid if photo else "", manual)
            replacements.append((image.start, image.end, replacement))
        for start, end, replacement in reversed(replacements):
            content = content[:start] + replacement + content[end:]
        return content
