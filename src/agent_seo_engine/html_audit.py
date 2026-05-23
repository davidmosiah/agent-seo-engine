"""HTML auditing helpers for SEO and accessibility signals."""

from __future__ import annotations

import re
from typing import Any

_IMG_TAG_RE = re.compile(r"<img\b[^>]*>", re.IGNORECASE | re.DOTALL)
_ALT_ATTR_RE = re.compile(
    r"""\balt\s*=\s*(?P<quote>["'])(?P<value>.*?)(?P=quote)""",
    re.IGNORECASE | re.DOTALL,
)
_UNQUOTED_ALT_RE = re.compile(r"""\balt\s*=\s*(?P<value>[^\s"'>]+)""", re.IGNORECASE)


def check_image_alt_coverage(html: str) -> dict[str, Any]:
    """Return alt-attribute coverage for ``<img>`` tags in ``html``.

    Counts each ``<img>`` tag in the document and reports how many carry a
    non-empty ``alt`` attribute. Returns a dict with ``total``, ``with_alt``,
    ``missing_alt``, ``coverage`` (ratio in 0..1) and ``missing`` (the offending
    tag fragments, truncated to a reasonable length for inspection).

    The implementation is intentionally regex-based to keep the package
    dependency-free; it handles single, double and unquoted alt values as well
    as ``alt=""`` (which counts as missing because it provides no accessibility
    or SEO signal beyond decorative use).
    """

    if not isinstance(html, str):
        raise TypeError("html must be a string")

    tags = _IMG_TAG_RE.findall(html)
    total = len(tags)

    if total == 0:
        return {
            "total": 0,
            "with_alt": 0,
            "missing_alt": 0,
            "coverage": 1.0,
            "missing": [],
        }

    with_alt = 0
    missing: list[str] = []
    for tag in tags:
        if _has_non_empty_alt(tag):
            with_alt += 1
        else:
            snippet = tag.strip()
            if len(snippet) > 160:
                snippet = snippet[:157] + "..."
            missing.append(snippet)

    coverage = round(with_alt / total, 4)
    return {
        "total": total,
        "with_alt": with_alt,
        "missing_alt": total - with_alt,
        "coverage": coverage,
        "missing": missing,
    }


def _has_non_empty_alt(tag: str) -> bool:
    match = _ALT_ATTR_RE.search(tag)
    if match is not None:
        return match.group("value").strip() != ""
    match = _UNQUOTED_ALT_RE.search(tag)
    if match is not None:
        return match.group("value").strip() != ""
    return False
