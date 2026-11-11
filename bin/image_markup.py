"""Shared parsing and rewriting for the inline images we publish."""

import html
import re
from dataclasses import dataclass
from urllib.parse import quote

MARKER = re.compile(
    r'[ \t]*<!-- photo-alt: ([A-Za-z0-9-]+)( manual)? -->'
)
IMAGE = re.compile(
    r'!\[(?P<alt>(?:\\.|[^\]\\])*)\]'
    r'\((?:<(?P<angle>[^>]+)>|(?P<path>[^\s()]+))\)'
    r'|!\[\[(?P<wiki>[^\]\n]+)\]\]'
    r'|<img\b[^>]*>',
    re.IGNORECASE,
)
ATTRIBUTE = re.compile(
    r'''(?<![\w:-])(src|alt)\s*=\s*(["'])(.*?)\2''', re.I | re.S,
)


def plain_text(text: str) -> str:
    return " ".join(text.split())


def markdown_alt(text: str) -> str:
    text = html.escape(plain_text(text), quote=False)
    return re.sub(r'([\\\[\]*_`])', r'\\\1', text)


def marker(uuid: str, manual: bool = False) -> str:
    return f" <!-- photo-alt: {uuid}{' manual' if manual else ''} -->"


@dataclass
class Image:
    start: int
    end: int
    path: str
    alt: str
    markup: str
    uuid: str = ""
    manual: bool = False

    def rewrite_path(self, path: str) -> str:
        if self.markup.lower().startswith("<img"):
            result = ATTRIBUTE.sub(
                lambda m: (f'{m[1]}={m[2]}{html.escape(quote(path), quote=True)}{m[2]}'
                           if m[1].lower() == "src" else m[0]),
                self.markup,
            )
        elif self.markup.startswith("![["):
            result = f"![](<{path}>)" if " " in path else f"![]({path})"
        else:
            match = IMAGE.match(self.markup)
            start, end = match.span("angle" if match["angle"] else "path")
            if match["angle"]:
                start, end = start - 1, end + 1
            replacement = f"<{path}>" if " " in path else path
            result = self.markup[:start] + replacement + self.markup[end:]
        return result + (marker(self.uuid, self.manual) if self.uuid else "")

    def render(self, alt: str, uuid: str = "", manual: bool = False) -> str:
        if manual and alt == self.alt:
            result = self.markup
        elif self.markup.lower().startswith("<img"):
            attribute = next(
                (m for m in ATTRIBUTE.finditer(self.markup)
                 if m[1].lower() == "alt"), None,
            )
            replacement = f'alt="{html.escape(plain_text(alt), quote=True)}"'
            if attribute:
                result = (self.markup[:attribute.start()] + replacement
                          + self.markup[attribute.end():])
            else:
                result = re.sub(r'\s*/?>$', lambda m: " " + replacement
                                + m[0], self.markup)
        else:
            path = f"<{self.path}>" if " " in self.path else self.path
            result = f"![{markdown_alt(alt)}]({path})"
        return result + (marker(uuid, manual) if uuid else "")


def images(content: str) -> list[Image]:
    """Read supported inline images, excluding code and HTML comments."""
    # Mask fenced code, then inline code and comments without moving offsets.
    masked = re.sub(
        r'(?ms)^ {0,3}(`{3,}|~{3,})[^\n]*\n.*?^ {0,3}\1[^\n]*(?:\n|$)',
        lambda m: " " * len(m[0]), content,
    )
    masked = re.sub(r'(`+).*?\1|<!--.*?-->',
                    lambda m: " " * len(m[0]), masked, flags=re.S)
    result = []
    for match in IMAGE.finditer(masked):
        match = IMAGE.match(content, match.start())
        if match is None:
            continue
        markup = content[match.start():match.end()]
        if markup.lower().startswith("<img"):
            attrs = {m[1].lower(): html.unescape(m[3])
                     for m in ATTRIBUTE.finditer(markup)}
            path, alt = attrs.get("src", ""), attrs.get("alt", "")
        else:
            path = match["angle"] or match["path"] or match["wiki"]
            alt = html.unescape(re.sub(r'\\(.)', r'\1', match["alt"] or ""))
        if not path:
            continue
        attached = MARKER.match(content, match.end())
        result.append(Image(
            match.start(), attached.end() if attached else match.end(),
            path, alt, markup, attached[1] if attached else "",
            bool(attached and attached[2]),
        ))
    return result
