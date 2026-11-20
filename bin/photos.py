"""Read photos, captions, and keywords from the local Photos library."""

import re
import sqlite3
import subprocess
from dataclasses import dataclass, field
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

# Keywords link to assets through a Core Data join table whose numbered
# table and column names change between macOS versions (e.g. Z_1KEYWORDS
# with columns Z_1ASSETATTRIBUTES and Z_53KEYWORDS).
KEYWORDS_TABLE = re.compile(r"Z_\d+KEYWORDS")


@dataclass
class Photo:
    uuid: str
    taken: datetime
    original_filename: str
    source: Path
    caption: str
    keywords: list[str] = field(default_factory=list)


def normalize_caption(caption: str) -> str:
    """Caption with every line break as \\n. Photos on iOS writes U+2028
    LINE SEPARATOR, which terminals don't display as a line break."""
    return "\n".join(caption.strip().splitlines())


def _image_source(row) -> Path:
    """The edited render if the photo was edited, else the original."""
    _, _, _, directory, filename, _, adjustments, _ = row
    if adjustments:
        uuid = row[0]
        renders = PHOTOS_LIBRARY / "resources" / "renders" / directory
        for render in sorted(renders.glob(f"{uuid}_1_201_a.*")):
            return render
    return PHOTOS_LIBRARY / "originals" / directory / filename


def _keywords_query(db: sqlite3.Connection) -> str:
    """A query for (asset UUID, keyword) rows in this library's layout."""
    tables = [
        name for (name,) in db.execute(
            "SELECT name FROM sqlite_master WHERE type = 'table'"
        )
        if KEYWORDS_TABLE.fullmatch(name)
    ]
    if len(tables) != 1:
        raise sqlite3.OperationalError(
            f"expected one keywords join table, found {tables or 'none'}"
        )
    table = tables[0]
    columns = [row[1] for row in db.execute(f"PRAGMA table_info({table})")]
    asset = [c for c in columns if c.endswith("ASSETATTRIBUTES")]
    keyword = [c for c in columns if KEYWORDS_TABLE.fullmatch(c)]
    if len(asset) != 1 or len(keyword) != 1:
        raise sqlite3.OperationalError(
            f"unexpected columns in {table}: {', '.join(columns)}"
        )
    return f"""
SELECT a.ZUUID, k.ZTITLE
FROM {table} j
JOIN ZKEYWORD k ON k.Z_PK = j.{keyword[0]}
JOIN ZADDITIONALASSETATTRIBUTES aa ON aa.Z_PK = j.{asset[0]}
JOIN ZASSET a ON a.Z_PK = aa.ZASSET
ORDER BY k.ZTITLE
"""


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
        keywords: dict[str, list[str]] = {}
        for uuid, keyword in db.execute(_keywords_query(db)):
            if keyword:
                keywords.setdefault(uuid, []).append(keyword)
    except sqlite3.OperationalError as e:
        raise RuntimeError(
            "couldn't read captions and keywords from the Photos library; "
            "its "
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
            caption=normalize_caption(caption or ""),
            keywords=keywords.get(uuid, []),
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



SET_KEYWORDS_SCRIPT = """
on run argv
  tell application "Photos"
    set keywords of media item id (item 1 of argv) to (rest of argv)
  end tell
end run
"""


def set_keywords(photo: Photo, keywords: list[str]) -> None:
    """Replace the photo's keywords in the Photos library."""
    subprocess.run(
        ["osascript", "-e", SET_KEYWORDS_SCRIPT, f"{photo.uuid}/L0/001",
         *keywords],
        check=True, capture_output=True,
    )
