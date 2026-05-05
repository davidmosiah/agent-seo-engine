from __future__ import annotations

import re
from typing import Any


def split_frontmatter(markdown: str) -> tuple[dict[str, Any], str]:
    if not markdown.startswith("---\n"):
        return {}, markdown
    parts = markdown.split("---\n", 2)
    if len(parts) < 3:
        return {}, markdown
    return _parse_simple_yaml(parts[1]), parts[2]


def score_markdown(markdown: str, primary_keyword: str = "", min_words: int = 900) -> dict[str, Any]:
    frontmatter, body = split_frontmatter(markdown)
    plain = _plain_text(body)
    words = re.findall(r"\b[\w'-]+\b", plain)
    word_count = len(words)
    h1 = re.findall(r"^#\s+(.+)$", body, flags=re.MULTILINE)
    h2 = re.findall(r"^##\s+(.+)$", body, flags=re.MULTILINE)
    links = re.findall(r"(?<!!)\[[^\]]+\]\(([^)\s]+)", body)
    internal_links = [link for link in links if link.startswith("/")]
    external_links = [link for link in links if link.startswith(("http://", "https://"))]

    title = str(frontmatter.get("title") or (h1[0] if h1 else "")).strip()
    description = str(frontmatter.get("description") or "").strip()
    keyword = primary_keyword.strip().lower()
    lower_body = plain.lower()
    keyword_count = lower_body.count(keyword) if keyword else 0
    density = round((keyword_count / word_count * 100), 2) if keyword and word_count else 0.0

    checks = {
        "title": _check(bool(title), 10, "Add a title or H1."),
        "title_length": _check(20 <= len(title) <= 70, 10, "Keep title between 20 and 70 characters."),
        "meta_description": _check(120 <= len(description) <= 165, 15, "Rewrite description to 120-165 characters."),
        "word_count": _check(word_count >= min_words, 15, f"Expand article to at least {min_words} words."),
        "h1": _check(len(h1) == 1, 10, "Use exactly one H1."),
        "h2_sections": _check(len(h2) >= 3, 10, "Add at least three H2 sections."),
        "keyword_in_title": _check(not keyword or keyword in title.lower(), 10, "Place the primary keyword in the title."),
        "keyword_in_first_100": _check(not keyword or keyword in " ".join(words[:100]).lower(), 10, "Use primary keyword in first 100 words."),
        "keyword_density": _check(not keyword or 0.4 <= density <= 2.5, 10, "Adjust primary keyword density to roughly 0.4%-2.5%."),
        "internal_links": _check(len(internal_links) >= 2, 5, "Add at least two internal links."),
        "external_links": _check(len(external_links) >= 1, 5, "Add at least one authoritative external link."),
    }

    max_score = sum(item["weight"] for item in checks.values())
    earned = sum(item["weight"] for item in checks.values() if item["passed"])
    score = round((earned / max_score) * 100, 1) if max_score else 0.0
    recommendations = [item["recommendation"] for item in checks.values() if not item["passed"]]

    return {
        "overall_score": score,
        "grade": _grade(score),
        "publishing_ready": score >= 85 and not any(
            not checks[key]["passed"] for key in ["title", "meta_description", "h1", "keyword_in_title"]
        ),
        "checks": checks,
        "metrics": {
            "word_count": word_count,
            "h1_count": len(h1),
            "h2_count": len(h2),
            "internal_link_count": len(internal_links),
            "external_link_count": len(external_links),
            "primary_keyword_occurrences": keyword_count,
            "primary_keyword_density": density,
        },
        "recommendations": recommendations,
    }


def _check(passed: bool, weight: int, recommendation: str) -> dict[str, Any]:
    return {"passed": passed, "weight": weight, "recommendation": recommendation}


def _grade(score: float) -> str:
    if score >= 90:
        return "A"
    if score >= 80:
        return "B"
    if score >= 70:
        return "C"
    if score >= 60:
        return "D"
    return "F"


def _plain_text(markdown: str) -> str:
    text = re.sub(r"```.*?```", "", markdown, flags=re.DOTALL)
    text = re.sub(r"^#+\s+", "", text, flags=re.MULTILINE)
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
    text = re.sub(r"[*_`>#-]", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def _parse_simple_yaml(block: str) -> dict[str, Any]:
    data: dict[str, Any] = {}
    current_key: str | None = None
    for raw in block.splitlines():
        line = raw.rstrip()
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if line.startswith("  - ") and current_key:
            data.setdefault(current_key, []).append(line[4:].strip().strip("\"'"))
            continue
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        key = key.strip()
        value = value.strip().strip("\"'")
        if value:
            data[key] = value
            current_key = None
        else:
            data[key] = []
            current_key = key
    return data
