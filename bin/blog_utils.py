"""
Shared utilities for blog publishing scripts.
"""

import re
import shutil
import subprocess
from datetime import datetime
from pathlib import Path

WIKI_DIR = Path.home() / "wiki"
BLOG_DIR = Path(__file__).parent.parent.resolve()
NOTES_DIR = BLOG_DIR / "_notes"
FEED_DIR = BLOG_DIR / "feed"
TAGS_DIR = BLOG_DIR / "tagged"
IMAGES_DIR = BLOG_DIR / "images"
BASE_URL = "https://unformeddelta.wiki"

TZ_OFFSETS = {
    "EST": "-0500",
    "EDT": "-0400",
    "CST": "-0600",
    "CDT": "-0500",
    "MST": "-0700",
    "MDT": "-0600",
    "PST": "-0800",
    "PDT": "-0700",
    "UTC": "+0000",
    "GMT": "+0000",
}


def parse_frontmatter(content: str) -> tuple[dict, str]:
    """Parse YAML frontmatter and return (metadata, body)."""
    if not content.startswith("---"):
        return {}, content

    parts = content.split("---", 2)
    if len(parts) < 3:
        return {}, content

    frontmatter_text = parts[1].strip()
    body = parts[2].lstrip("\n")

    metadata = {}
    for line in frontmatter_text.split("\n"):
        if ":" in line:
            key, value = line.split(":", 1)
            metadata[key.strip()] = value.strip()

    return metadata, body


def local_tz_offset() -> str:
    """Get the local timezone offset as a string like '+0900' or '-0500'."""
    return datetime.now().astimezone().strftime("%z")


def convert_date(date_str: str) -> str:
    """Convert date from note format to Jekyll format."""
    fallback = local_tz_offset()

    match = re.match(
        r"(\d{4}-\d{2}-\d{2})T(\d{2}:\d{2})[-]?([A-Z]{3,4})", date_str
    )
    if match:
        date_part, time_part, tz_abbrev = match.groups()
        offset = TZ_OFFSETS.get(tz_abbrev, fallback)
        return f"{date_part} {time_part} {offset}"

    match = re.match(r"(\d{4}-\d{2}-\d{2})T(\d{2}:\d{2})([-+]\d{4})?", date_str)
    if match:
        date_part, time_part, offset = match.groups()
        offset = offset or fallback
        return f"{date_part} {time_part} {offset}"

    return date_str


def slugify(title: str) -> str:
    """Convert title to URL-friendly slug."""
    slug = title.lower()
    slug = slug.replace("/", "-")
    slug = re.sub(r"[^\w\s-]", "", slug)
    slug = re.sub(r"[\s_]+", "-", slug)
    slug = slug.strip("-")
    slug = re.sub(r"-+", "-", slug)
    return slug


def get_published_url(note_id: str) -> str | None:
    """Check if a note is published and return its permalink.

    Determines publication status by checking if a blog note exists
    in _notes/, rather than relying on wiki frontmatter.
    """
    blog_path = find_blog_note(note_id)
    if not blog_path:
        return None
    slug = blog_path.stem.removeprefix(f"{note_id}-")
    return f"/{note_id}/{slug}"


def resolve_wikilinks(body: str) -> str:
    """
    Resolve wiki-links in the body.
    [[id|text]] or [[id|text]]<!--wls--> -> [text](url) if published,
    otherwise just text
    """
    pattern = r"\[\[([A-Za-z0-9]+)\|([^\]]+)\]\](?:<!--wls-->)?"

    def replace_wikilink(match):
        note_id = match.group(1)
        text = match.group(2)
        published_url = get_published_url(note_id)
        if published_url:
            return f"[{text}]({published_url})"
        else:
            return text

    return re.sub(pattern, replace_wikilink, body)


def extract_title(body: str) -> tuple[str, str]:
    """Extract title from # heading and return (title, body_without_title)."""
    lines = body.split("\n")
    for i, line in enumerate(lines):
        if line.startswith("# "):
            title = line[2:].strip()
            # Remove backticks (they don't render correctly in titles)
            title = title.replace("`", "")
            # Remove the title line and any following blank lines
            remaining = lines[i + 1 :]
            while remaining and not remaining[0].strip():
                remaining.pop(0)
            return title, "\n".join(remaining)
    return "", body


def parse_tags(tags_str: str) -> list[str]:
    """Parse tags from frontmatter value."""
    if not tags_str:
        return []
    # Handle both [tag1, tag2] and tag1, tag2 formats
    tags_str = tags_str.strip("[]")
    return [t.strip() for t in tags_str.split(",") if t.strip()]


def find_blog_note(note_id: str) -> Path | None:
    """Find the blog note file for a given note ID (handles slug in filename)."""
    matches = list(NOTES_DIR.glob(f"{note_id}*.md"))
    if len(matches) == 1:
        return matches[0]
    elif len(matches) > 1:
        for m in matches:
            if m.stem == note_id:
                return m
        return sorted(matches, key=lambda p: len(p.name))[0]
    return None


def extract_note_id(filename: str) -> str:
    """Extract note ID from filename like 'de14645c-slug-here.md'."""
    stem = filename.removesuffix(".md")
    match = re.match(r"^([A-Za-z0-9]{8,12})(?:-|$)", stem)
    if match:
        return match.group(1)
    return stem


def get_blog_tags(note_id: str) -> list[str]:
    """Get current tags from the blog version of the note."""
    blog_path = find_blog_note(note_id)
    if not blog_path:
        return []

    content = blog_path.read_text()
    metadata, _ = parse_frontmatter(content)
    return parse_tags(metadata.get("tags", ""))


def ensure_published_link(wiki_path: Path, published_url: str) -> bool:
    """Ensure the wiki note has the correct published: URL."""
    content = wiki_path.read_text()
    metadata, body = parse_frontmatter(content)

    current_url = metadata.get("published", "")
    if current_url == published_url:
        return False

    if not content.startswith("---"):
        new_content = f"---\npublished: {published_url}\n---\n\n{content}"
    elif "published:" in content:
        new_content = re.sub(
            r"published:\s*[^\n]*",
            f"published: {published_url}",
            content
        )
    else:
        lines = content.split("\n")
        lines.insert(1, f"published: {published_url}")
        new_content = "\n".join(lines)

    if new_content != content:
        wiki_path.write_text(new_content)
        return True
    return False


def update_wiki_tags(wiki_path: Path, tags: list[str]):
    """Update the tags in a wiki note's frontmatter."""
    content = wiki_path.read_text()
    metadata, body = parse_frontmatter(content)

    current_tags = parse_tags(metadata.get("tags", ""))
    if set(current_tags) == set(tags):
        return False

    tags_str = f"[{', '.join(tags)}]" if tags else ""

    if not content.startswith("---"):
        if tags:
            new_content = f"---\ntags: {tags_str}\n---\n\n{content}"
        else:
            new_content = content
    elif re.search(r"^tags:\s*", content, re.MULTILINE):
        if tags:
            new_content = re.sub(
                r"^tags:\s*[^\n]*",
                f"tags: {tags_str}",
                content,
                flags=re.MULTILINE
            )
        else:
            new_content = re.sub(
                r"^tags:\s*[^\n]*\n?",
                "",
                content,
                flags=re.MULTILINE
            )
    else:
        if tags:
            lines = content.split("\n")
            lines.insert(1, f"tags: {tags_str}")
            new_content = "\n".join(lines)
        else:
            new_content = content

    if new_content != content:
        wiki_path.write_text(new_content)
        return True
    return False


def collect_all_tags() -> set[str]:
    """Collect all tags used across published notes."""
    tags = set()
    for note_path in NOTES_DIR.glob("*.md"):
        content = note_path.read_text()
        metadata, _ = parse_frontmatter(content)
        tags.update(parse_tags(metadata.get("tags", "")))
    return tags


def sync_tag_feeds(tags: set[str] | None = None):
    """Ensure a feed file exists for every tag used in notes."""
    FEED_DIR.mkdir(exist_ok=True)
    if tags is None:
        tags = collect_all_tags()

    created = []
    for tag in sorted(tags):
        feed_path = FEED_DIR / f"{tag}.xml"
        if not feed_path.exists():
            feed_path.write_text(
                f"---\nlayout: feed\n"
                f"feed_suffix: \"{tag}\"\n"
                f"feed_tag: \"{tag}\"\n---\n"
            )
            created.append(tag)
    if created:
        print(f"Created feed(s): {', '.join(created)}")


TAG_PAGE_TEMPLATE = """\
---
layout: note-index
title: "Unformed Delta — {tag}"
description: "Posts tagged {tag}"
active_tag: "{tag}"
nav_exclude: true
---
"""


def sync_tag_pages(tags: set[str] | None = None):
    """Ensure a tag index page exists for every tag used in notes."""
    TAGS_DIR.mkdir(exist_ok=True)
    if tags is None:
        tags = collect_all_tags()

    created = []
    for tag in sorted(tags):
        tag_dir = TAGS_DIR / tag
        tag_page = tag_dir / "index.html"
        if tag_page.exists():
            continue
        tag_dir.mkdir(exist_ok=True)
        tag_page.write_text(TAG_PAGE_TEMPLATE.format(tag=tag))
        created.append(tag)
    if created:
        print(f"Created tag page(s): {', '.join(created)}")


def sync_all_tag_artifacts():
    """Sync feeds and tag pages for all tags used in notes."""
    tags = collect_all_tags()
    sync_tag_feeds(tags)
    sync_tag_pages(tags)


def build_frontmatter(
    note_id: str,
    title: str,
    date: str,
    tags: list[str],
    wiki_meta: dict,
    extra_redirects: set[str] | None = None,
) -> str:
    """Build Jekyll frontmatter string."""
    slug = slugify(title)
    permalink = f"/{note_id}/{slug}"

    lines = [
        "---",
        "layout: post",
        f"title: \"{title}\"",
        f"date: {date}",
        f"permalink: {permalink}",
        "redirect_from:",
        f"  - /{note_id}",
    ]

    for redirect in sorted(extra_redirects or []):
        entry = f"  - {redirect}"
        if redirect != f"/{note_id}" and entry not in lines:
            lines.append(entry)

    if tags:
        lines.append(f"tags: [{', '.join(tags)}]")

    wiki_image = wiki_meta.get("image", "").strip()
    if wiki_image:
        dest = blog_image_name(note_id, Path(wiki_image))
        lines.append(f"image: /images/{dest}")

    lines.append("---")
    return "\n".join(lines)


def blog_image_name(note_id: str, source: Path) -> str:
    """Compute the blog-side filename for a wiki image."""
    if source.suffix.lower() == ".heic":
        return f"{note_id}-{source.stem}.jpeg"
    return f"{note_id}-{source.name}"


def extract_image_paths(body: str) -> list[str]:
    """
    Extract image paths from markdown content.

    Handles:
      - ![alt](path) - standard markdown
      - ![alt](<path>) - markdown with angle brackets (allows spaces)
      - ![[path]] - Obsidian-style wikilinks
    """
    paths = []

    # Angle-bracket paths: ![alt](<path with spaces>)
    angle_pattern = r'!\[[^\]]*\]\(<([^>]+)>\)'
    for match in re.finditer(angle_pattern, body):
        paths.append(match.group(1))

    # Standard markdown images without angle brackets: ![alt](path)
    std_pattern = r'!\[[^\]]*\]\(([^)<>\s]+)\)'
    for match in re.finditer(std_pattern, body):
        paths.append(match.group(1))

    # Obsidian-style wikilinks: ![[path]]
    obsidian_pattern = r'!\[\[([^\]]+)\]\]'
    for match in re.finditer(obsidian_pattern, body):
        paths.append(match.group(1))

    return paths


def scrub_metadata(image_path: Path) -> None:
    """Strip all metadata (GPS, device info, etc.) from an image."""
    subprocess.run(
        ["exiftool", "-all=", "--icc_profile:all",
         "-overwrite_original", str(image_path)],
        check=True,
        capture_output=True,
    )


def copy_images(body: str, note_id: str) -> tuple[str, list[Path]]:
    """
    Copy images referenced in the body from wiki to blog.

    Returns:
        Tuple of (updated body with fixed paths, list of copied image paths)
    """
    image_paths = extract_image_paths(body)
    copied = []

    for img_path in image_paths:
        # Resolve the source path relative to wiki directory
        # Handle various path formats
        clean_path = img_path.replace("%20", " ")

        if clean_path.startswith("./"):
            clean_path = clean_path[2:]

        source = WIKI_DIR / clean_path
        if not source.exists():
            # Try without URL encoding
            source = WIKI_DIR / img_path
        if not source.exists():
            print(f"  Warning: image not found: {img_path}")
            continue

        # Determine destination filename (prefix with note_id for uniqueness)
        dest_name = blog_image_name(note_id, source)
        dest = IMAGES_DIR / dest_name

        # Copy (or convert) if not already there or if source is newer
        if not dest.exists() or source.stat().st_mtime > dest.stat().st_mtime:
            if source.suffix.lower() == ".heic":
                subprocess.run(
                    ["sips", "-s", "format", "jpeg",
                     str(source), "--out", str(dest)],
                    check=True,
                    capture_output=True,
                )
            else:
                shutil.copy2(source, dest)
            scrub_metadata(dest)
            copied.append(dest)

        # Update the path in the body to point to the blog images directory
        # Wrap in angle brackets to handle spaces in filenames
        new_path = f"</images/{dest_name}>"

        # Replace the original path with the new one
        # Handle both regular and angle-bracket syntax
        old_patterns = [
            re.escape(img_path),
            re.escape(f"<{img_path}>"),
            re.escape(img_path.replace(" ", "%20")),
        ]
        for pattern in old_patterns:
            body = re.sub(
                rf'(!\[[^\]]*\]\()<?{pattern}>?(\))',
                rf'\g<1>{new_path}\2',
                body
            )

        # Handle Obsidian-style wikilinks - convert to standard markdown
        body = re.sub(
            rf'!\[\[{re.escape(img_path)}\]\]',
            f'![]({new_path})',
            body
        )

    return body, copied
