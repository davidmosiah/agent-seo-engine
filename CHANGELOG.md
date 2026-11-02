# Changelog

## 0.1.3 - Candidate

- Restore compatibility with the patched MCP 1.x SDK (`mcp>=1.30.0,<2`).
- Refresh dependency lock and test supported Python versions with a TOML fallback.

## 0.1.2 - 2026-08-29

Skill layer ships in-package (`skill/SKILL.md`). CLI `call <tool>` maps to the same MCP tool handlers.

## 0.1.1 - 2026-05-22
- Add `check_image_alt_coverage(html)` HTML auditor returning total/with_alt/missing counts, coverage ratio, and offending tag snippets.
- Export `check_image_alt_coverage` from package root.

## 0.1.0
- Initial release.
