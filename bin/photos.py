"""Read photos and captions from the local Photos library."""

import sqlite3
import subprocess
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path

PHOTOS_LIBRARY = Path.home() / "Pictures" / "Photos Library.photoslibrary"
# Core Data timestamps count seconds from 2001-01-01 UTC.
CORE_DATA_EPOCH = datetime(2001, 1, 1, tzinfo=timezone.utc)

# Still images (ZKIND = 0) that are not trashed or hidden.
PHOTOS_QUERY = """
SELECT a.ZUUID, a.ZDATECREATED, aa.ZTIMEZONEOFFSET, a.ZDIRECTORY,
       a.ZFILENAME, aa.ZORIGINALFILENAME, a.ZADJUSTMENTSSTATE,
       d.ZLONGDESCRIPTION
FROM ZASSET a
JOIN ZADDITIONALASSETATTRIBUTES aa ON aa.ZASSET = a.Z_PK
LEFT JOIN ZASSETDESCRIPTION d ON d.ZASSETATTRIBUTES = aa.Z_PK
WHERE a.ZKIND = 0 AND a.ZTRASHEDSTATE = 0 AND a.ZHIDDEN = 0
ORDER BY a.ZDATECREATED DESC
"""


@dataclass
class Photo:
    uuid: str
    taken: datetime
    original_filename: str
    source: Path
    caption: str


def _image_source(row) -> Path:
    """The edited render if the photo was edited, else the original."""
    _, _, _, directory, filename, _, adjustments, _ = row
    if adjustments:
        uuid = row[0]
        renders = PHOTOS_LIBRARY / "resources" / "renders" / directory
        for render in sorted(renders.glob(f"{uuid}_1_201_a.*")):
            return render
    return PHOTOS_LIBRARY / "originals" / directory / filename


def load_photos() -> list[Photo]:
    """Read visible still photos, including ones with cleared captions."""
    db_path = PHOTOS_LIBRARY / "database" / "Photos.sqlite"
    if not db_path.exists():
        raise FileNotFoundError(f"Photos library not found at {PHOTOS_LIBRARY}")
    try:
        db = sqlite3.connect(f"file:{db_path}?mode=ro", uri=True)
    except sqlite3.OperationalError as e:
        raise RuntimeError(f"couldn't open the Photos library database: {e}") from e
    try:
        rows = db.execute(PHOTOS_QUERY).fetchall()
    except sqlite3.OperationalError as e:
        raise RuntimeError(
            "couldn't read captions from the Photos library; its "
            f"database layout may have changed in a macOS update ({e})"
        )
    finally:
        db.close()

    photos = []
    for row in rows:
        uuid, created, tz_offset, *_, original, _, caption = row
        tz = timezone(timedelta(seconds=tz_offset or 0))
        taken = (CORE_DATA_EPOCH + timedelta(seconds=created)).astimezone(tz)
        photos.append(Photo(
            uuid=uuid,
            taken=taken,
            original_filename=original or row[4],
            source=_image_source(row),
            caption=(caption or "").strip(),
        ))
    return photos


# Photos.app identifies media items as "<uuid>/L0/001".
SET_CAPTION_SCRIPT = """
on run argv
  tell application "Photos"
    set description of media item id (item 1 of argv) to (item 2 of argv)
  end tell
end run
"""


def set_caption(photo: Photo, caption: str) -> None:
    """Save caption to the photo in the Photos library."""
    subprocess.run(
        ["osascript", "-e", SET_CAPTION_SCRIPT, f"{photo.uuid}/L0/001",
         caption],
        check=True, capture_output=True,
    )

