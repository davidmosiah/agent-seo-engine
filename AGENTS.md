# Agent Development Notes

## Scope

This repo is a Python CLI plus optional MCP server for agent-first SEO scoring, intent classification and opportunity prioritization.

## Commands

- Install dev deps: `pip install -e ".[dev]"`
- Test: `pytest`
- Build package: `python -m build`
- Check dist: `twine check dist/*`
- CLI smoke: `agent-seo-engine doctor`

## Rules

- Never commit private analytics exports, customer drafts, API keys, or credentials.
- Keep CLI output deterministic and JSON-first unless `--format markdown` is requested.
- Keep PyPI publishing on Trusted Publishing; do not add long-lived PyPI tokens.
- Keep MCP tools dry-run/local-first by default.
