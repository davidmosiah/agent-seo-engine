# Contributing

Contributions are welcome around deterministic SEO scoring, intent classification, opportunity ranking, MCP ergonomics, tests and docs.

## Local development

```bash
pip install -e ".[dev]"
pytest
python -m build
twine check dist/*
```

## Design rules

- Keep CLI output deterministic and JSON-first unless markdown is requested.
- Never commit private analytics exports, customer drafts, API keys or credentials.
- Keep MCP tools local-first and dry-run friendly.
- Keep PyPI publishing on Trusted Publishing; do not add long-lived PyPI tokens.

## Pull request checklist

- `pytest` passes.
- Package builds successfully when packaging metadata changes.
- README, `llms.txt` and examples are updated when commands or tools change.
